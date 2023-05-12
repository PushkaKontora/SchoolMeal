from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request

from app.auth.presentation.errors import NotFoundRefreshTokenInCookiesError
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
