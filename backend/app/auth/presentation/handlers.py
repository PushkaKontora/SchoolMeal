from typing import cast

from fastapi import Body, Request, Response

from app.auth.domain.entities import AccessTokenOut, LoginSchema
from app.auth.domain.exceptions import (
    BadCredentialsException,
    InvalidTokenSignatureException,
    NotFoundRefreshTokenException,
    RefreshWithRevokedTokenException,
    TokenExpirationException,
)
from app.auth.domain.services import AuthService
from app.auth.presentation.exceptions import (
    InvalidBearerCredentialsException,
    NotFoundRefreshCookieException,
    UnauthorizedException,
)
from app.config import JWTSettings
from app.entities import SuccessResponse
from app.exceptions import ExceptionHandler


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
        )

        return cast(AccessTokenOut, tokens)

    async def logout(self, request: Request, response: Response) -> SuccessResponse:
        refresh_token = request.cookies.get(self._jwt_settings.refresh_token_cookie)

        if not refresh_token:
            raise NotFoundRefreshCookieException

        await self._auth_service.logout(refresh_token)
        response.delete_cookie(self._jwt_settings.refresh_token_cookie)

        return SuccessResponse()

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


class InvalidTokenSignatureHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return InvalidTokenSignatureException

    @property
    def message(self) -> str:
        return "The token's signature was destroyed"


class RefreshWithRevokedTokenHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return RefreshWithRevokedTokenException

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


class NotFoundRefreshTokenHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return NotFoundRefreshTokenException

    @property
    def message(self) -> str:
        return "The token was not created or was deleted by the service"


class UnauthorizedHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return UnauthorizedException

    @property
    def message(self) -> str:
        return "Permission denied"

    @property
    def status_code(self) -> int:
        return 403


class InvalidBearerCredentialsHandler(ExceptionHandler):
    @property
    def exception(self) -> type[Exception]:
        return InvalidBearerCredentialsException

    @property
    def message(self) -> str:
        return "Invalid Authorization header"
