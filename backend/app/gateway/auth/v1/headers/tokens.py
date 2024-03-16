from typing import Annotated
from uuid import UUID

from fastapi import Cookie
from starlette.responses import Response

from app.gateway.auth.v1.view import AccessTokenOut
from app.identity.api.dto import SessionOut


_COOKIE_NAME = "refresh"


def send_tokens_to_user(response: Response, session: SessionOut) -> AccessTokenOut:
    response.set_cookie(
        key=_COOKIE_NAME,
        value=str(session.refresh_token),
        expires=int(session.expires_in.timestamp()),
        path="/api/auth",
        httponly=True,
    )

    return AccessTokenOut(token=session.access_token)


def clear_cookies(response: Response) -> Response:
    response.delete_cookie(key=_COOKIE_NAME)

    return response


RefreshTokenDep = Annotated[UUID, Cookie(alias=_COOKIE_NAME, include_in_schema=False)]
