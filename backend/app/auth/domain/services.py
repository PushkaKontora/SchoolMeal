from datetime import datetime, timedelta

import bcrypt
import jwt
from dependency_injector.wiring import Provide, inject

from app.auth.db.issued_token.filters import ByUserId as TokenByUserId, ByValue
from app.auth.db.issued_token.model import IssuedToken
from app.auth.db.password.filters import ByUserId as PasswordByUserId
from app.auth.domain.entities import JWTPayload, JWTTokens, TokenType
from app.auth.domain.exceptions import (
    BadCredentialsException,
    InvalidTokenSignatureException,
    NotFoundRefreshTokenException,
    RefreshWithRevokedTokenException,
    TokenExpirationException,
    UnknownTokenTypeException,
)
from app.config import JWTSettings, PasswordSettings
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.users.db.user.filters import ByLogin
from app.users.db.user.model import Role


class AuthService:
    def __init__(self, password_service: "PasswordService", jwt_service: "JWTService"):
        self._password_service = password_service
        self._jwt_service = jwt_service

    @inject
    async def signin(self, login: str, password: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> JWTTokens:
        async with uow:
            user = await uow.users_repo.find_one(ByLogin(login))
            hashed_password = (await uow.passwords_repo.get_last(PasswordByUserId(user.id))).value if user else None

            if not user or not hashed_password or not self._password_service.check_password(password, hashed_password):
                raise BadCredentialsException

            tokens = self._create_tokens(user.id, user.role, uow)

            await uow.commit()

            return tokens

    @inject
    async def logout(self, refresh_token: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> None:
        if not self._jwt_service.try_decode(refresh_token):
            raise InvalidTokenSignatureException

        async with uow:
            await uow.issued_tokens_repo.revoke(ByValue(refresh_token))
            await uow.commit()

    @inject
    async def refresh_tokens(self, refresh_token: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> JWTTokens:
        payload = self._jwt_service.try_decode(refresh_token)

        if not payload:
            raise InvalidTokenSignatureException

        async with uow:
            token = await uow.issued_tokens_repo.find_one(ByValue(refresh_token))
            if not token:
                raise NotFoundRefreshTokenException

            if token.revoked:
                await uow.issued_tokens_repo.revoke(TokenByUserId(token.user_id))
                await uow.commit()

                raise RefreshWithRevokedTokenException

            token.revoked = True

            if self._jwt_service.is_token_expired(token.created_at, TokenType.REFRESH):
                await uow.commit()
                raise TokenExpirationException

            tokens = self._create_tokens(payload.user_id, payload.role, uow)

            await uow.commit()

            return tokens

    def _create_tokens(self, user_id: int, role: Role, uow: UnitOfWork) -> JWTTokens:
        tokens = self._jwt_service.generate_tokens(user_id, role)

        uow.issued_tokens_repo.save(IssuedToken(user_id=user_id, value=tokens.refresh_token))

        return tokens


class JWTService:
    def __init__(self, jwt_settings: JWTSettings):
        self._jwt_settings = jwt_settings

    def decode_access_token(self, token: str) -> JWTPayload:
        payload = self.try_decode(token)

        if not payload or payload.type != TokenType.ACCESS:
            raise InvalidTokenSignatureException

        if self.is_token_expired_in(payload.expires_in):
            raise TokenExpirationException

        return payload

    def generate_tokens(self, user_id: int, role: Role) -> JWTTokens:
        tokens = JWTTokens(
            access_token=self.generate_token(TokenType.ACCESS, user_id, role),
            refresh_token=self.generate_token(TokenType.REFRESH, user_id, role),
        )

        return tokens

    def generate_token(self, token_type: TokenType, user_id: int, role: Role) -> str:
        ttl = self._get_token_ttl(token_type)

        payload = JWTPayload(
            type=token_type, user_id=user_id, role=role, expires_in=int((datetime.utcnow() + ttl).timestamp())
        )
        secret, algorithm = self._jwt_settings.secret.get_secret_value(), self._jwt_settings.algorithm

        return jwt.encode(payload.dict(), secret, algorithm)

    def try_decode(self, token: str) -> JWTPayload | None:
        try:
            payload = jwt.decode(
                token, key=self._jwt_settings.secret.get_secret_value(), algorithms=[self._jwt_settings.algorithm]
            )
        except jwt.PyJWTError:
            return None

        return JWTPayload(**payload)

    def is_token_expired(self, created_at: datetime, token_type: TokenType) -> bool:
        return datetime.utcnow() >= created_at + self._get_token_ttl(token_type)

    def is_token_expired_in(self, timestamp: float) -> bool:
        return datetime.utcnow().timestamp() >= timestamp

    def _get_token_ttl(self, token_type: TokenType) -> timedelta:
        match token_type:
            case TokenType.ACCESS:
                return self._jwt_settings.access_token_ttl

            case TokenType.REFRESH:
                return self._jwt_settings.refresh_token_ttl

        raise UnknownTokenTypeException


class PasswordService:
    def __init__(self, password_settings: PasswordSettings):
        self.settings = password_settings

    def check_password(self, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode(self.settings.encoding), hashed_password)

    def make_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt(self.settings.rounds)

        return bcrypt.hashpw(password.encode(self.settings.encoding), salt)
