from ipaddress import IPv4Address
from uuid import UUID

from app.user_management.application.authorizations.abc import IAuthorization
from app.user_management.application.dao import ISessionRepository, IUserRepository
from app.user_management.application.dto import AuthenticationIn, RefreshTokensIn
from app.user_management.application.limiters import IBruteForceLimiter
from app.user_management.domain.jwt import AccessToken, Fingerprint, Session
from app.user_management.domain.rest import Method
from app.user_management.domain.user import User


async def authenticate(
    dto: AuthenticationIn,
    user_repository: IUserRepository,
    session_repository: ISessionRepository,
    limiter: IBruteForceLimiter,
) -> tuple[AccessToken, Session] | None:
    user = await user_repository.get_by_login(dto.login)

    if not user or not user.password.verify(dto.password) or limiter.is_ip_banned(dto.ip):
        limiter.increase_attempts(dto.ip)
        return None

    limiter.reset(dto.ip)

    return await _open_session(user, ip=dto.ip, fingerprint=dto.fingerprint, session_repository=session_repository)


async def refresh_tokens(
    dto: RefreshTokensIn, session_repository: ISessionRepository, user_repository: IUserRepository
) -> tuple[AccessToken, Session] | None:
    session = await session_repository.pop(id_=dto.token)

    if not session:
        return None

    user = await user_repository.get_by_id(id_=session.user_id)

    if not user or session.is_expired or dto.fingerprint != session.fingerprint:
        await session_repository.remove_all_by_user_id(user_id=session.user_id)
        return None

    return await _open_session(user, ip=dto.ip, fingerprint=dto.fingerprint, session_repository=session_repository)


async def logout(token: UUID, session_repository: ISessionRepository) -> None:
    await session_repository.pop(id_=token)


def authorize(token: str, uri: str, method: Method, secret: str, authorization: IAuthorization) -> AccessToken | None:
    if not (access_token := AccessToken.decode(token, secret)):
        return None

    return access_token if authorization.authorize(access_token, uri, method) else None


async def _open_session(
    user: User, ip: IPv4Address, fingerprint: Fingerprint, session_repository: ISessionRepository
) -> tuple[AccessToken, Session]:
    access_token = AccessToken.generate(user)
    session = Session.generate(user, ip, fingerprint)

    if await session_repository.count_by_user_id(user.id) >= 5:
        await session_repository.remove_all_by_user_id(user.id)

    await session_repository.add(session)

    return access_token, session
