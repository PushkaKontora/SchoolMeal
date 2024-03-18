from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Response, status

from app.identity.api.client_ip import ClientIPDep
from app.identity.api.request import RequestMethodDep, RequestURIDep
from app.identity.api.schema import AccessTokenOut, LoginBody, RefreshBody
from app.identity.api.tokens import AccessTokenDep, RefreshTokenDep, clear_cookies, set_session_in_cookie
from app.identity.application import services
from app.identity.application.authorizations.abc import IAuthorization
from app.identity.application.dao import ISessionRepository, IUserRepository
from app.identity.application.dto import AuthenticationIn, RefreshTokensIn
from app.identity.application.limiters import IBruteForceLimiter
from app.identity.domain.credentials import Login, Password
from app.identity.domain.jwt import Fingerprint, Secret
from app.identity.infrastructure.config import JWTConfig
from app.identity.infrastructure.dependencies import IdentityContainer
from app.shared.api import responses
from app.shared.api.errors import BadRequest, Forbidden, UnprocessableEntity
from app.shared.fastapi.schemas import AuthorizedUser, OKSchema


router = APIRouter()


@router.post(
    "/login",
    summary="Аутентифицировать пользователя",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
@inject
async def login(
    response: Response,
    body: Annotated[LoginBody, Body()],
    ip: ClientIPDep,
    config: JWTConfig = Depends(Provide[IdentityContainer.jwt_config]),
    user_repository: IUserRepository = Depends(Provide[IdentityContainer.user_repository]),
    session_repository: ISessionRepository = Depends(Provide[IdentityContainer.session_repository]),
    limiter: IBruteForceLimiter = Depends(Provide[IdentityContainer.limiter]),
) -> AccessTokenOut:
    try:
        login_ = Login(body.login)
        password = Password(body.password)
        fingerprint = Fingerprint(body.fingerprint)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    dto = AuthenticationIn(
        login=login_, password=password, ip=ip, fingerprint=fingerprint, secret=Secret(config.secret)
    )
    result = await services.authenticate(dto, user_repository, session_repository, limiter)

    if not result:
        raise BadRequest("Пользователь не был аутентифицирован")

    token, session = result

    set_session_in_cookie(response, session)

    return AccessTokenOut.from_model(token)


@router.post(
    "/refresh",
    summary="Перевыпустить токены",
    status_code=status.HTTP_200_OK,
    responses=responses.UNPROCESSABLE_ENTITY | responses.BAD_REQUEST,
)
@inject
async def refresh(
    response: Response,
    body: Annotated[RefreshBody, Body()],
    token: RefreshTokenDep,
    ip: ClientIPDep,
    config: JWTConfig = Depends(Provide[IdentityContainer.jwt_config]),
    user_repository: IUserRepository = Depends(Provide[IdentityContainer.user_repository]),
    session_repository: ISessionRepository = Depends(Provide[IdentityContainer.session_repository]),
) -> AccessTokenOut:
    try:
        fingerprint = Fingerprint(body.fingerprint)
    except ValueError as error:
        raise UnprocessableEntity(str(error))

    dto = RefreshTokensIn(token=token, ip=ip, fingerprint=fingerprint, secret=Secret(config.secret))
    result = await services.refresh_tokens(dto, session_repository, user_repository)

    if not result:
        raise BadRequest("Сессия не была обновлена")

    access_token, session = result

    set_session_in_cookie(response, session)

    return AccessTokenOut.from_model(access_token)


@router.post(
    "/logout",
    summary="Выйти из аккаунта",
    status_code=status.HTTP_200_OK,
)
@inject
async def logout(
    response: Response,
    token: RefreshTokenDep,
    session_repository: ISessionRepository = Depends(Provide[IdentityContainer.session_repository]),
) -> OKSchema:
    await services.logout(token, session_repository)

    clear_cookies(response)

    return OKSchema()


@router.get(
    "/authorize",
    summary="Авторизация",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.FORBIDDEN,
    include_in_schema=False,
)
@inject
async def authorize(
    token: AccessTokenDep,
    uri: RequestURIDep,
    method: RequestMethodDep,
    config: JWTConfig = Depends(Provide[IdentityContainer.jwt_config]),
    authorization: IAuthorization = Depends(Provide[IdentityContainer.authorization]),
) -> Response:
    payload = services.authorize(token, uri, method, secret=Secret(config.secret), authorization=authorization)

    if not payload:
        raise Forbidden

    user = AuthorizedUser(id=payload.user_id, role=payload.role)

    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={"X-User": user.json()})
