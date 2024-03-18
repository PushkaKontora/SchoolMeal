from ipaddress import IPv4Address
from uuid import UUID

from app.identity.application.authorizations.abc import IAuthorization
from app.identity.application.dao import ISessionRepository, IUserRepository
from app.identity.application.dto import AuthenticationIn, RefreshTokensIn
from app.identity.application.limiters import IBruteForceLimiter
from app.identity.domain.jwt import AccessToken, Fingerprint, Payload, Secret, Session
from app.identity.domain.rest import Method
from app.identity.domain.user import User


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

    return await _open_session(
        user, ip=dto.ip, fingerprint=dto.fingerprint, secret=dto.secret, session_repository=session_repository
    )


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

    return await _open_session(
        user, ip=dto.ip, fingerprint=dto.fingerprint, secret=dto.secret, session_repository=session_repository
    )


async def logout(token: UUID, session_repository: ISessionRepository) -> None:
    await session_repository.pop(id_=token)


def authorize(token: str, uri: str, method: Method, secret: Secret, authorization: IAuthorization) -> Payload | None:
    if not (payload := AccessToken.decode(token, secret)):
        return None

    return payload if authorization.authorize(payload, uri, method) else None


async def _open_session(
    user: User, ip: IPv4Address, fingerprint: Fingerprint, secret: Secret, session_repository: ISessionRepository
) -> tuple[AccessToken, Session]:
    access_token = AccessToken.generate(user, secret)
    session = Session.generate(user, ip, fingerprint)

    if await session_repository.count_by_user_id(user.id) >= 5:
        await session_repository.remove_all_by_user_id(user.id)

    await session_repository.add(session)

    return access_token, session
