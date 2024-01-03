from typing import Annotated

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import Response

from app.users.domain.tokens import RefreshToken


REFRESH_COOKIE = "refresh"


def _get_refresh_token(token: Annotated[str, Cookie(alias=REFRESH_COOKIE, include_in_schema=False)]) -> str:
    return token


def _get_access_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> str:
    return authorization.credentials


def set_refresh_in_cookies(response: Response, refresh_token: RefreshToken, secret: str) -> Response:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=refresh_token.encode(secret),
        expires=int(refresh_token.exp.timestamp()),
        httponly=True,
    )

    return response


def delete_refresh_from_cookies(response: Response) -> Response:
    response.delete_cookie(key=REFRESH_COOKIE)

    return response


AccessTokenDep = Annotated[str, Depends(_get_access_token)]
RefreshTokenDep = Annotated[str, Depends(_get_refresh_token)]
