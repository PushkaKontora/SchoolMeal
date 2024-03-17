from ipaddress import IPv4Address
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.identity.api import errors
from app.identity.api.dto import SessionOut
from app.identity.application import services
from app.identity.application.authorizations.abc import IAuthorization
from app.identity.application.dao import ISessionRepository, IUserRepository
from app.identity.application.dto import AuthenticationIn, RefreshTokensIn
from app.identity.application.limiters import IBruteForceLimiter
from app.identity.domain.credentials import Login, Password
from app.identity.domain.jwt import Fingerprint, Payload, Secret
from app.identity.domain.rest import Method
from app.identity.infrastructure.config import JWTConfig
from app.identity.infrastructure.dependencies import IdentityContainer
from app.shared.api.errors import DomainValidationError


@inject
async def authenticate(
    login: str,
    password: str,
    ip: IPv4Address,
    fingerprint: str,
    config: JWTConfig = Provide[IdentityContainer.jwt_config],
    user_repository: IUserRepository = Provide[IdentityContainer.user_repository],
    session_repository: ISessionRepository = Provide[IdentityContainer.session_repository],
    limiter: IBruteForceLimiter = Provide[IdentityContainer.limiter],
) -> Result[SessionOut, DomainValidationError | errors.NotAuthenticated]:
    try:
        login_ = Login(login)
        password_ = Password(password)
        fingerprint_ = Fingerprint(fingerprint)
        secret = Secret(config.secret)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    dto = AuthenticationIn(login=login_, password=password_, ip=ip, fingerprint=fingerprint_, secret=secret)
    session = await services.authenticate(dto, user_repository, session_repository, limiter)

    if not session:
        return Err(errors.NotAuthenticated())

    return Ok(SessionOut.from_application(session))


@inject
async def refresh_tokens(
    token: UUID,
    ip: IPv4Address,
    fingerprint: str,
    config: JWTConfig = Provide[IdentityContainer.jwt_config],
    user_repository: IUserRepository = Provide[IdentityContainer.user_repository],
    session_repository: ISessionRepository = Provide[IdentityContainer.session_repository],
) -> Result[SessionOut, DomainValidationError | errors.NotRefreshed]:
    try:
        fingerprint_ = Fingerprint(fingerprint)
        secret = Secret(config.secret)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    dto = RefreshTokensIn(token=token, ip=ip, fingerprint=fingerprint_, secret=secret)
    session = await services.refresh_tokens(dto, session_repository, user_repository)

    if not session:
        return Err(errors.NotRefreshed())

    return Ok(SessionOut.from_application(session))


@inject
async def logout(
    token: UUID,
    session_repository: ISessionRepository = Provide[IdentityContainer.session_repository],
) -> None:
    await services.logout(token, session_repository)


@inject
def authorize(
    token: str,
    uri: str,
    method: Method,
    config: JWTConfig = Provide[IdentityContainer.jwt_config],
    authorization: IAuthorization = Provide[IdentityContainer.authorization],
) -> Payload | None:
    return services.authorize(token, uri, method, Secret(config.secret), authorization)
