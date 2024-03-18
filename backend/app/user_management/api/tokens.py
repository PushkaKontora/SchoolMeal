from typing import Annotated
from uuid import UUID

from fastapi import Cookie, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import Response

from app.user_management.domain.jwt import Session


_COOKIE_NAME = "refresh"


def set_session_in_cookie(response: Response, session: Session) -> Response:
    response.set_cookie(
        key=_COOKIE_NAME,
        value=str(session.id.value),
        expires=int(session.expires_in.timestamp()),
        path="/api/users",
        httponly=True,
    )

    return response


def clear_cookies(response: Response) -> Response:
    response.delete_cookie(key=_COOKIE_NAME)

    return response


def _get_access_token(authorization: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]) -> str:
    return authorization.credentials


AccessTokenDep = Annotated[str, Depends(_get_access_token)]
RefreshTokenDep = Annotated[UUID, Cookie(alias=_COOKIE_NAME, include_in_schema=False)]
