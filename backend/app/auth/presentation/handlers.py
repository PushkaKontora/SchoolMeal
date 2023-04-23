from typing import cast

from fastapi import Body, Request, Response

from app.auth.domain.entities import AccessTokenOut, LoginSchema
from app.auth.domain.services import AuthService
from app.auth.presentation.exceptions import NotFoundRefreshCookieException
from app.base_entity import SuccessResponse
from app.config import JWTSettings


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
