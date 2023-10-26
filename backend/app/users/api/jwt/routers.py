from fastapi import APIRouter, Response

from app.common.api.dependencies import SessionDep
from app.common.api.errors import AuthenticateError, LogicError, ValidationModelError
from app.common.api.schemas import HTTPError, OKSchema
from app.users.api.dependencies.repositories import SessionsRepositoryDep, UsersRepositoryDep
from app.users.api.dependencies.tokens import (
    AccessTokenDep,
    RefreshTokenDep,
    add_refresh_in_cookies,
    delete_refresh_from_cookies,
)
from app.users.api.jwt.schemas import AccessTokenOut, CredentialIn, InvalidCredentialError
from app.users.application.use_cases.jwt import IncorrectLoginOrPasswordError, authenticate, logout, refresh_tokens
from app.users.domain.session import AlreadySessionRevokedError


router = APIRouter()


@router.post(
    "/authenticate",
    summary="Аутентификация по логину и паролю",
    status_code=200,
    responses={401: {"model": HTTPError}, 422: {"model": HTTPError}},
)
async def authenticate_(
    response: Response,
    session: SessionDep,
    credential: CredentialIn,
    users_repository: UsersRepositoryDep,
    sessions_repository: SessionsRepositoryDep,
) -> AccessTokenOut:
    try:
        login, password = credential.to_model()

        async with session.begin():
            access, refresh = await authenticate(login, password, users_repository, sessions_repository)

    except InvalidCredentialError as error:
        raise ValidationModelError(detail=str(error))

    except IncorrectLoginOrPasswordError as error:
        raise AuthenticateError(detail=str(error))

    add_refresh_in_cookies(response, refresh)

    return AccessTokenOut.from_model(access)


@router.post(
    "/logout",
    summary="Выход из аккаунта",
    status_code=200,
    responses={422: {"model": HTTPError}},
)
async def logout_(
    response: Response,
    session: SessionDep,
    access_token: AccessTokenDep,
    sessions_repository: SessionsRepositoryDep,
) -> OKSchema:
    async with session.begin():
        await logout(access_token, sessions_repository)

    delete_refresh_from_cookies(response)

    return OKSchema()


@router.post(
    "/refresh-tokens",
    summary="Перевыпустить токены",
    status_code=200,
    responses={400: {"model": HTTPError}, 422: {"model": HTTPError}},
)
async def refresh_tokens_(
    response: Response, session: SessionDep, refresh_token: RefreshTokenDep, sessions_repository: SessionsRepositoryDep
) -> AccessTokenOut:
    async with session.begin():
        try:
            access, refresh = await refresh_tokens(refresh_token, sessions_repository)

        except AlreadySessionRevokedError as error:
            await session.commit()
            raise LogicError(detail=str(error)) from error

    add_refresh_in_cookies(response, refresh)

    return AccessTokenOut.from_model(access)
