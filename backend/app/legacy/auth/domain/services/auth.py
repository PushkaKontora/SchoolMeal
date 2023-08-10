from dependency_injector.wiring import Provide, inject

from app.legacy.auth.db.issued_token.filters import ByUserId as TokenByUserId, ByValue
from app.legacy.auth.db.issued_token.model import IssuedToken
from app.legacy.auth.db.password.filters import ByUserId as PasswordByUserId
from app.legacy.auth.db.password.model import Password
from app.legacy.auth.db.password.sorters import SortByCreationDateDESC
from app.legacy.auth.domain.entities import CredentialsIn, JWTTokensOut, TokenType
from app.legacy.auth.domain.errors import (
    BadCredentialsError,
    InvalidTokenSignatureError,
    NotFoundRefreshTokenError,
    RefreshUsingRevokedTokenError,
    TokenExpirationError,
)
from app.legacy.auth.domain.services.jwt import generate_tokens, is_token_expired, try_decode
from app.legacy.auth.domain.services.password import check_password
from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.users.db.user.filters import ByLogin
from app.legacy.users.db.user.model import Role, User


@inject
async def authenticate(
    credentials: CredentialsIn, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> JWTTokensOut:
    async with uow:
        user = await uow.repository(User).find_first(ByLogin(credentials.login))
        if not user:
            raise BadCredentialsError

        password = await uow.repository(Password).find_first(PasswordByUserId(user.id), SortByCreationDateDESC())
        if not password or not check_password(credentials.password, password.value):
            raise BadCredentialsError

        tokens = _create_tokens(user.id, user.role, uow)

        await uow.commit()

        return tokens


@inject
async def revoke_refresh_token(token: str, uow: UnitOfWork = Provide[AppContainer.unit_of_work]) -> None:
    if not try_decode(token):
        raise InvalidTokenSignatureError

    async with uow:
        await uow.repository(IssuedToken).update(ByValue(token), revoked=True)
        await uow.commit()


@inject
async def update_tokens_using_refresh_token(
    token: str, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> JWTTokensOut:
    payload = try_decode(token)

    if not payload:
        raise InvalidTokenSignatureError

    async with uow:
        token = await uow.repository(IssuedToken).find_first(ByValue(token))
        if not token:
            raise NotFoundRefreshTokenError

        if token.revoked:
            await uow.repository(IssuedToken).update(TokenByUserId(token.user_id), revoked=True)
            await uow.commit()

            raise RefreshUsingRevokedTokenError

        token.revoked = True

        if is_token_expired(token.created_at, TokenType.REFRESH):
            await uow.commit()
            raise TokenExpirationError

        tokens = _create_tokens(payload.user_id, payload.role, uow)

        await uow.commit()

        return tokens


def _create_tokens(user_id: int, role: Role, uow: UnitOfWork) -> JWTTokensOut:
    tokens = generate_tokens(user_id, role)

    uow.repository(IssuedToken).save(IssuedToken(user_id=user_id, value=tokens.refresh_token))

    return tokens
