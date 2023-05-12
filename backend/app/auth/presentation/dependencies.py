from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from app.auth.domain.entities import JWTPayload
from app.auth.domain.services.jwt import decode_access_token
from app.auth.presentation.errors import (
    InvalidAuthorizationHeaderError,
    NotFoundRefreshTokenInCookiesError,
    UnauthorizedError,
)
from app.config import JWTSettings
from app.container import Container


@inject
def get_refresh_token_from_cookies(
    request: Request, settings: JWTSettings = Depends(Provide[Container.jwt_settings])
) -> str:
    refresh_token = request.cookies.get(settings.refresh_token_cookie)

    if not refresh_token:
        raise NotFoundRefreshTokenInCookiesError

    return refresh_token


class JWTAuth(HTTPBearer):
    def __init__(self, header: str = "Authorization", scheme: str = "Bearer"):
        super().__init__(bearerFormat=scheme, scheme_name="JWT", auto_error=False)
        self._header = header
        self._scheme = scheme

    async def __call__(self, request: Request) -> JWTPayload:
        authorization = request.headers.get(self._header)
        scheme, access_token = get_authorization_scheme_param(authorization)

        if not (authorization and scheme and access_token) or scheme.lower() != self._scheme.lower():
            raise InvalidAuthorizationHeaderError

        payload = decode_access_token(access_token)

        if not self.authorize(payload):
            raise UnauthorizedError

        return payload

    def authorize(self, payload: JWTPayload) -> bool:
        return True
