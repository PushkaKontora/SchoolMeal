from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import Response

from app.common.api.errors import ValidationModelError
from app.common.infrastructure.settings import jwt
from app.users.domain.tokens import AccessToken, InvalidTokenError, RefreshToken


REFRESH_COOKIE = "refresh"


def _get_refresh_token(token: Annotated[str, Cookie(alias=REFRESH_COOKIE, include_in_schema=False)]) -> RefreshToken:
    try:
        refresh = RefreshToken.decode(token, jwt.secret.get_secret_value())

    except InvalidTokenError as error:
        raise ValidationModelError(detail=str(error)) from error

    return refresh


def _get_access_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> AccessToken:
    try:
        access = AccessToken.decode(authorization.credentials, jwt.secret.get_secret_value())

    except InvalidTokenError as error:
        raise ValidationModelError(detail=str(error)) from error

    return access


def add_refresh_in_cookies(response: Response, refresh: RefreshToken) -> Response:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=refresh.encode(jwt.secret.get_secret_value()),
        expires=int(refresh.exp.timestamp()),
        httponly=True,
    )

    return response


def delete_refresh_from_cookies(response: Response) -> Response:
    response.delete_cookie(key=REFRESH_COOKIE)

    return response


AccessTokenDep = Annotated[AccessToken, Depends(_get_access_token)]
RefreshTokenDep = Annotated[RefreshToken, Depends(_get_refresh_token)]
