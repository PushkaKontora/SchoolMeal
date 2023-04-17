from typing import cast

from fastapi import Body, Request, Response

from app.auth.domain.entities import AccessTokenOut, LoginSchema
from app.auth.domain.exceptions import (
    BadCredentialsException,
    TokenExpirationException,
    TokenIsRevokedException,
    TokenSignatureException,
    UnknownTokenException,
)
from app.auth.domain.services import AuthService
from app.auth.presentation.exceptions import NotFoundRefreshCookieException
from app.config import JWTSettings
from app.exceptions import ExceptionHandler
from app.responses import Success


class AuthHandlers:
    def __init__(self, auth_service: AuthService, jwt_settings: JWTSettings):
        self._auth_service = auth_service
        self._jwt_settings = jwt_settings

    async def signin(self, response: Response, credentials: LoginSchema = Body(...)) -> AccessTokenOut:
        tokens = await self._auth_service.signin(credentials.login, credentials.password)

        response.set_cookie(
            key=self._jwt_settings.refresh_token_cookie,
            value=tokens.refresh_token,
            httponly=True,
            domain=self._jwt_settings.domain,
        )

        return cast(AccessTokenOut, tokens)

    async def logout(self, request: Request, response: Response) -> Success:
        refresh_token = request.cookies.get(self._jwt_settings.refresh_token_cookie)

        if not refresh_token:
            raise NotFoundRefreshCookieException

        await self._auth_service.logout(refresh_token)
        response.delete_cookie(self._jwt_settings.refresh_token_cookie)

        return Success()

    async def refresh_tokens(self, request: Request, response: Response) -> AccessTokenOut:
        refresh_token = request.cookies.get(self._jwt_settings.refresh_token_cookie)

        if not refresh_token:
            raise NotFoundRefreshCookieException

        tokens = await self._auth_service.refresh_tokens(refresh_token)

        response.set_cookie(
            key=self._jwt_settings.refresh_token_cookie,
            value=tokens.refresh_token,
            httponly=True,
        )

        return cast(AccessTokenOut, tokens)


class BadCredentialsHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return BadCredentialsException

    @property
    def message(self) -> str:
        return "Incorrect login or password"

    @property
    def status_code(self) -> int:
        return 401


class NotFoundRefreshCookieHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return NotFoundRefreshCookieException

    @property
    def message(self) -> str:
        return "A refresh token is not found in cookies"


class TokenSignatureHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return TokenSignatureException

    @property
    def message(self) -> str:
        return "The token's signature was damaged"


class TokenIsRevokedHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return TokenIsRevokedException

    @property
    def message(self) -> str:
        return "The token is already revoked"


class TokenExpirationHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return TokenExpirationException

    @property
    def message(self) -> str:
        return "The token expired"


class UnknownTokenHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return UnknownTokenException

    @property
    def message(self) -> str:
        return "The token was not created by the service"
