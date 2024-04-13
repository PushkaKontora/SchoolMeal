from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends, Response, status

from app.shared.api import responses
from app.shared.api.errors import BadRequest, Forbidden, UnprocessableEntity
from app.shared.api.schemas import AuthorizedUser, OKSchema
from app.user_management.api.client_ip import ClientIPDep
from app.user_management.api.request import RequestMethodDep, RequestURIDep
from app.user_management.api.schema import AccessTokenOut, LoginBody, RefreshBody
from app.user_management.api.tokens import AccessTokenDep, RefreshTokenDep, clear_cookies, set_session_in_cookie
from app.user_management.application import services
from app.user_management.application.authorization import IAuthorization
from app.user_management.application.dao import ISessionRepository, IUserRepository
from app.user_management.application.dto import AuthenticationIn, RefreshTokensIn
from app.user_management.application.limiters import IBruteForceLimiter
from app.user_management.domain.credentials import Login, Password
from app.user_management.domain.jwt import Fingerprint
from app.user_management.infrastructure.config import Config
from app.user_management.infrastructure.dependencies import IdentityContainer


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
    config: Config = Depends(Provide[IdentityContainer.config]),
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

    result = await services.authenticate(
        dto=AuthenticationIn(login=login_, password=password, ip=ip, fingerprint=fingerprint),
        user_repository=user_repository,
        session_repository=session_repository,
        limiter=limiter,
    )

    if not result:
        raise BadRequest("Пользователь не был аутентифицирован")

    token, session = result

    set_session_in_cookie(response, session, domain=config.domain)

    return AccessTokenOut.from_model(token, secret=config.jwt_secret)


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
    config: Config = Depends(Provide[IdentityContainer.config]),
    user_repository: IUserRepository = Depends(Provide[IdentityContainer.user_repository]),
    session_repository: ISessionRepository = Depends(Provide[IdentityContainer.session_repository]),
) -> AccessTokenOut:
    try:
        fingerprint = Fingerprint(body.fingerprint)
    except ValueError as error:
        raise UnprocessableEntity(str(error))

    result = await services.refresh_tokens(
        dto=RefreshTokensIn(token=token, ip=ip, fingerprint=fingerprint),
        session_repository=session_repository,
        user_repository=user_repository,
    )

    if not result:
        raise BadRequest("Сессия не была обновлена")

    access_token, session = result

    set_session_in_cookie(response, session, domain=config.domain)

    return AccessTokenOut.from_model(access_token, secret=config.jwt_secret)


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
    config: Config = Depends(Provide[IdentityContainer.config]),
    authorization: IAuthorization = Depends(Provide[IdentityContainer.authorization]),
) -> Response:
    access_token = services.authorize(token, uri, method, secret=config.jwt_secret, authorization=authorization)

    if not access_token:
        raise Forbidden

    payload = access_token.payload
    user = AuthorizedUser(id=payload.user_id, role=payload.role)

    return Response(status_code=status.HTTP_204_NO_CONTENT, headers={"X-User": user.json()})
