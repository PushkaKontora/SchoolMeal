from datetime import datetime, timedelta

import bcrypt
import jwt
from dependency_injector.wiring import Provide, inject

from app.auth.db.specifications import IssuedTokensFilter, PasswordsFilter
from app.auth.domain.entities import IssuedToken, JWTTokens, TokenType
from app.auth.domain.exceptions import (
    BadCredentialsException,
    TokenExpirationException,
    TokenIsRevokedException,
    TokenSignatureException,
    UnknownTokenException,
    UnknownTokenTypeException,
)
from app.config import JWTSettings
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.entities import BaseEntity
from app.users.db.specifications import UsersFilter
from app.users.domain.entities import Role


class Payload(BaseEntity):
    type: TokenType
    user_id: int
    role: Role
    expires_in: int


class AuthService:
    def __init__(self, passwords_service: "PasswordsService", jwt_service: "JWTService"):
        self._passwords_service = passwords_service
        self._jwt_service = jwt_service

    @inject
    async def signin(self, login: str, password: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> JWTTokens:
        async with uow:
            user = await uow.users_repo.find_one(UsersFilter.ByLogin(login))

            if not user or not await self._passwords_service.verify_password(user.id, password, uow):
                raise BadCredentialsException

            return await self._jwt_service.create_tokens(user.id, user.role, uow)

    @inject
    async def logout(self, refresh_token: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> None:
        payload = self._jwt_service.try_decode(refresh_token)

        if not payload:
            raise TokenSignatureException

        async with uow:
            await self._jwt_service.revoke_refresh_token(refresh_token, uow, can_others=False)

    @inject
    async def refresh_tokens(self, refresh_token: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> JWTTokens:
        payload = self._jwt_service.try_decode(refresh_token)

        if not payload:
            raise TokenSignatureException

        async with uow:
            token = await self._jwt_service.revoke_refresh_token(refresh_token, uow, can_others=True)

            if self._jwt_service.expires(token.created_at, TokenType.REFRESH):
                raise TokenExpirationException

            return await self._jwt_service.create_tokens(payload.user_id, payload.role, uow)


class PasswordsService:
    async def verify_password(self, user_id: int, password: str, uow: UnitOfWork) -> bool:
        expected = await uow.passwords_repo.get_last(PasswordsFilter.ByUserId(user_id))

        return expected and self.check_password(password, expected.value)

    @staticmethod
    def check_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


class JWTService:
    def __init__(self, jwt_settings: JWTSettings):
        self._jwt_settings = jwt_settings

    async def create_tokens(self, user_id: int, role: Role, uow: UnitOfWork) -> JWTTokens:
        tokens = JWTTokens(
            access_token=self.generate_token(TokenType.ACCESS, user_id, role),
            refresh_token=self.generate_token(TokenType.REFRESH, user_id, role),
        )

        uow.issued_tokens_repo.create(user_id, tokens.refresh_token)
        await uow.commit()

        return tokens

    async def revoke_refresh_token(self, value: str, uow: UnitOfWork, can_others: bool = True) -> IssuedToken:
        token = await uow.issued_tokens_repo.find_one(IssuedTokensFilter.ByValue(value))
        if not token:
            raise UnknownTokenException

        if token.revoked and can_others:
            await uow.issued_tokens_repo.revoke(IssuedTokensFilter.ByUserId(token.user_id))
            await uow.commit()

            raise TokenIsRevokedException

        await uow.issued_tokens_repo.revoke(IssuedTokensFilter.ByValue(token.value))
        await uow.commit()

        return token.copy(update={"revoked": True})

    def generate_token(self, token_type: TokenType, user_id: int, role: Role) -> str:
        ttl = self._get_token_ttl(token_type)

        payload = Payload(
            type=token_type, user_id=user_id, role=role, expires_in=int((datetime.utcnow() + ttl).timestamp())
        )
        secret, algorithm = self._jwt_settings.secret.get_secret_value(), self._jwt_settings.algorithm

        return jwt.encode(payload.dict(), secret, algorithm)

    def try_decode(self, token: str) -> Payload | None:
        try:
            payload = jwt.decode(
                token, key=self._jwt_settings.secret.get_secret_value(), algorithms=[self._jwt_settings.algorithm]
            )
        except jwt.PyJWTError:
            return None

        return Payload(**payload)

    def expires(self, created_at: datetime, token_type: TokenType) -> bool:
        return datetime.utcnow() >= created_at + self._get_token_ttl(token_type)

    def _get_token_ttl(self, token_type: TokenType) -> timedelta:
        match token_type:
            case TokenType.ACCESS:
                return self._jwt_settings.access_token_ttl

            case TokenType.REFRESH:
                return self._jwt_settings.refresh_token_ttl

        raise UnknownTokenTypeException
