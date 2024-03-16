from ipaddress import IPv4Address
from uuid import UUID

from app.identity.application.dao import ISessionRepository, IUserRepository
from app.identity.application.dto import AuthenticationIn, RefreshTokensIn, SessionOut
from app.identity.domain.jwt import AccessToken, Fingerprint, Secret, Session
from app.identity.domain.user import User


async def authenticate(
    dto: AuthenticationIn, user_repository: IUserRepository, session_repository: ISessionRepository
) -> SessionOut | None:
    user = await user_repository.get_by_login(dto.login)

    if not user or not user.password.verify(dto.password):
        return None

    return await _open_session(
        user, ip=dto.ip, fingerprint=dto.fingerprint, secret=dto.secret, session_repository=session_repository
    )


async def refresh_tokens(
    dto: RefreshTokensIn, session_repository: ISessionRepository, user_repository: IUserRepository
) -> SessionOut | None:
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


async def _open_session(
    user: User, ip: IPv4Address, fingerprint: Fingerprint, secret: Secret, session_repository: ISessionRepository
) -> SessionOut:
    access_token = AccessToken.generate(user, secret)
    session = Session.generate(user, ip, fingerprint)

    if await session_repository.count_by_user_id(user.id) >= 5:
        await session_repository.remove_all_by_user_id(user.id)

    await session_repository.add(session)

    return SessionOut(
        access_token=access_token,
        refresh_token=session.id,
        expires_in=session.expires_in,
        created_at=session.created_at,
    )
