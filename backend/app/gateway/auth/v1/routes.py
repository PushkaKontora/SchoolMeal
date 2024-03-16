from typing import Annotated

from fastapi import APIRouter, Body, Response
from result import Err

from app.gateway import responses
from app.gateway.auth.v1.dto import LoginBody, RefreshBody
from app.gateway.auth.v1.headers.client_ip import ClientIPDep
from app.gateway.auth.v1.headers.tokens import RefreshTokenDep, clear_cookies, send_tokens_to_user
from app.gateway.auth.v1.view import AccessTokenOut
from app.gateway.errors import BadRequest, UnprocessableEntity
from app.identity.api import handlers as identity_api
from app.identity.api.errors import NotAuthenticated, NotRefreshed
from app.shared.api.errors import DomainValidationError
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/login",
    summary="Аутентифицировать пользователя",
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
async def login(response: Response, body: Annotated[LoginBody, Body()], ip: ClientIPDep) -> AccessTokenOut:
    result = await identity_api.authenticate(
        login=body.login, password=body.password, fingerprint=body.fingerprint, ip=ip
    )

    match result:
        case Err(DomainValidationError(message=message)):
            raise UnprocessableEntity(message)

        case Err(NotAuthenticated(message=message)):
            raise BadRequest(message)

    return send_tokens_to_user(response, session=result.unwrap())


@router.post(
    "/refresh",
    summary="Перевыпустить токены",
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
async def refresh(
    response: Response, body: Annotated[RefreshBody, Body()], token: RefreshTokenDep, ip: ClientIPDep
) -> AccessTokenOut:
    result = await identity_api.refresh_tokens(token=token, ip=ip, fingerprint=body.fingerprint)

    match result:
        case Err(DomainValidationError(message=message)):
            raise UnprocessableEntity(message)

        case Err(NotRefreshed(message=message)):
            raise BadRequest(message)

    return send_tokens_to_user(response, session=result.unwrap())


@router.post(
    "/logout",
    summary="Выйти из аккаунта",
    responses=responses.BAD_REQUEST,
)
async def logout(response: Response, token: RefreshTokenDep) -> OKSchema:
    await identity_api.logout(token)

    clear_cookies(response)

    return OKSchema()
