from datetime import datetime, timezone
from ipaddress import IPv4Address

from fastapi import APIRouter, Body, Depends
from starlette import status
from starlette.responses import Response

from app.common.gateway.responses import response_400, response_401, response_404, response_422
from app.config import jwt
from app.user.application.services import UserService
from app.user.domain.errors import (
    EmptyLoginError,
    EmptyPasswordError,
    InvalidTokenError,
    NotFoundUserError,
    NotVerifiedPasswordError,
    RevokedTokenError,
    TokenExpirationError,
)
from app.user.domain.model import RefreshToken
from app.user.gateway.rest.auth.dependencies import get_refresh_token_from_cookies, get_remote_ip
from app.user.gateway.rest.auth.dto import AccessTokenOut, CredentialsIn
from app.user.gateway.rest.auth.errors import (
    InvalidRefreshTokenError,
    LoginValidationError,
    PasswordValidationError,
    WrongLoginOrPasswordError,
)
from app.user.gateway.rest.dependencies import get_user_service


router = APIRouter()


@router.post(
    path="/authenticate",
    summary="Аутентификация пользователя по логину и паролю",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenOut,
    responses=response_401 | response_404 | response_422,  # type: ignore
)
async def authenticate(
    response: Response,
    credentials: CredentialsIn = Body(),
    ip: IPv4Address = Depends(get_remote_ip),
    user_service: UserService = Depends(get_user_service),
) -> AccessTokenOut:
    try:
        tokens = await user_service.authenticate(login=credentials.login, password=credentials.password, ip=ip)

    except EmptyLoginError as error:
        raise LoginValidationError from error

    except EmptyPasswordError as error:
        raise PasswordValidationError from error

    except (NotFoundUserError, NotVerifiedPasswordError) as error:
        raise WrongLoginOrPasswordError from error

    _set_refresh_token_cookie_to_cookies(response, tokens.refresh)

    return AccessTokenOut(access_token=str(tokens.access))


@router.post(
    path="/reissue-tokens",
    summary="Обновление пары токенов с помощью рефреш-токена",
    status_code=status.HTTP_200_OK,
    response_model=AccessTokenOut,
    responses=response_400 | response_422,  # type: ignore
)
async def reissue_tokens(
    response: Response,
    refresh_token: str = Depends(get_refresh_token_from_cookies),
    ip: IPv4Address = Depends(get_remote_ip),
    user_service: UserService = Depends(get_user_service),
) -> AccessTokenOut:
    try:
        tokens = await user_service.reissue_tokens(refresh_token=refresh_token, ip=ip)

    except (InvalidTokenError, NotFoundUserError, RevokedTokenError, TokenExpirationError) as error:
        raise InvalidRefreshTokenError from error

    _set_refresh_token_cookie_to_cookies(response, tokens.refresh)

    return AccessTokenOut(access_token=str(tokens.access))


def _set_refresh_token_cookie_to_cookies(response: Response, token: RefreshToken) -> None:
    response.set_cookie(
        key=jwt.refresh_token_cookie,
        value=str(token),
        httponly=True,
        expires=datetime.now(timezone.utc) + jwt.refresh_token_ttl,
    )
