from dependency_injector.wiring import Provide, inject

from app.auth.db.issued_token.filters import ByUserId as TokenByUserId, ByValue
from app.auth.db.issued_token.model import IssuedToken
from app.auth.db.password.filters import ByUserId as PasswordByUserId
from app.auth.domain.entities import CredentialsIn, JWTTokensOut, TokenType
from app.auth.domain.exceptions import (
    BadCredentialsException,
    InvalidTokenSignatureException,
    NotFoundRefreshTokenException,
    RefreshWithRevokedTokenException,
    TokenExpirationException,
)
from app.auth.domain.services.jwt import generate_tokens, is_token_expired, try_decode
from app.auth.domain.services.password import check_password
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.users.db.user.filters import ByLogin
from app.users.db.user.model import Role


@inject
async def authenticate(credentials: CredentialsIn, uow: UnitOfWork = Provide[Database.unit_of_work]) -> JWTTokensOut:
    async with uow:
        user = await uow.users_repo.find_one(ByLogin(credentials.login))
        hashed_password = (await uow.passwords_repo.get_last(PasswordByUserId(user.id))).value if user else None

        if not user or not hashed_password or not check_password(credentials.password, hashed_password):
            raise BadCredentialsException

        tokens = _create_tokens(user.id, user.role, uow)

        await uow.commit()

        return tokens


@inject
async def revoke_refresh_token(token: str, uow: UnitOfWork = Provide[Database.unit_of_work]) -> None:
    if not try_decode(token):
        raise InvalidTokenSignatureException

    async with uow:
        await uow.issued_tokens_repo.revoke(ByValue(token))
        await uow.commit()


@inject
async def update_tokens_using_refresh_token(
    token: str, uow: UnitOfWork = Provide[Database.unit_of_work]
) -> JWTTokensOut:
    payload = try_decode(token)

    if not payload:
        raise InvalidTokenSignatureException

    async with uow:
        token = await uow.issued_tokens_repo.find_one(ByValue(token))
        if not token:
            raise NotFoundRefreshTokenException

        if token.revoked:
            await uow.issued_tokens_repo.revoke(TokenByUserId(token.user_id))
            await uow.commit()

            raise RefreshWithRevokedTokenException

        token.revoked = True

        if is_token_expired(token.created_at, TokenType.REFRESH):
            await uow.commit()
            raise TokenExpirationException

        tokens = _create_tokens(payload.user_id, payload.role, uow)

        await uow.commit()

        return tokens


def _create_tokens(user_id: int, role: Role, uow: UnitOfWork) -> JWTTokensOut:
    tokens = generate_tokens(user_id, role)

    uow.issued_tokens_repo.save(IssuedToken(user_id=user_id, value=tokens.refresh_token))

    return tokens
