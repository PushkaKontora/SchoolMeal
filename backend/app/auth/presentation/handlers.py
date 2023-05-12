from dependency_injector.wiring import Provide, inject
from fastapi import Body, Depends, Response

from app.auth.domain.entities import AccessTokenOut, CredentialsIn
from app.auth.domain.services.auth import authenticate, revoke_refresh_token, update_tokens_using_refresh_token
from app.auth.presentation.dependencies import get_refresh_token_from_cookies
from app.config import JWTSettings
from app.container import Container
from app.responses import SuccessResponse


@inject
async def signin(
    response: Response,
    credentials: CredentialsIn = Body(),
    settings: JWTSettings = Depends(Provide[Container.jwt_settings]),
) -> AccessTokenOut:
    tokens = await authenticate(credentials)

    response.set_cookie(
        key=settings.refresh_token_cookie,
        value=tokens.refresh_token,
        httponly=True,
    )

    return tokens


@inject
async def logout(
    response: Response,
    token: str = Depends(get_refresh_token_from_cookies),
    settings: JWTSettings = Depends(Provide[Container.jwt_settings]),
) -> SuccessResponse:
    await revoke_refresh_token(token)

    response.delete_cookie(settings.refresh_token_cookie)

    return SuccessResponse()


@inject
async def refresh_tokens(
    response: Response,
    token: str = Depends(get_refresh_token_from_cookies),
    settings: JWTSettings = Depends(Provide[Container.jwt_settings]),
) -> AccessTokenOut:
    tokens = await update_tokens_using_refresh_token(token)

    response.set_cookie(
        key=settings.refresh_token_cookie,
        value=tokens.refresh_token,
        httponly=True,
    )

    return tokens
