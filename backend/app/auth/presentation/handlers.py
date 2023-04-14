from typing import cast

from fastapi import Body, Response

from app.auth.domain.entities import AuthenticationOut, LoginSchema
from app.auth.domain.exceptions import BadCredentialsException
from app.auth.domain.services import AuthService
from app.config import JWTSettings
from app.exceptions import DomainExceptionHandler


class AuthHandlers:
    def __init__(self, auth_service: AuthService, jwt_settings: JWTSettings):
        self._auth_service = auth_service
        self._jwt_settings = jwt_settings

    async def signin(self, response: Response, credentials: LoginSchema = Body(...)) -> AuthenticationOut:
        tokens = await self._auth_service.signin(credentials.login, credentials.password)

        response.set_cookie(
            key=self._jwt_settings.refresh_token_header,
            value=tokens.refresh_token,
            httponly=True,
            domain=self._jwt_settings.domain,
        )

        return cast(AuthenticationOut, tokens)


class BadCredentialsHandler(DomainExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return BadCredentialsException

    @property
    def message(self) -> str:
        return "Incorrect login or password"

    @property
    def status_code(self) -> int:
        return 401
