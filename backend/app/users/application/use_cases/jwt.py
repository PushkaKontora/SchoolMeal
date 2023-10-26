from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.users.application.repositories import ISessionsRepository, IUsersRepository, NotFoundUserError
from app.users.domain.login import Login
from app.users.domain.passwords import Password
from app.users.domain.session import AlreadySessionRevokedError, Session
from app.users.domain.tokens import AccessToken, RefreshToken
from app.users.domain.user import NotVerifiedPasswordError


class IncorrectLoginOrPasswordError(Exception):
    pass


async def authenticate(
    login: Login,
    password: Password,
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
) -> tuple[AccessToken, RefreshToken]:
    """
    :raise IncorrectLoginOrPasswordError: неправильный логин или пароль
    """

    try:
        user = await users_repository.get_by_login(login)

        authenticated_user = user.authenticate(password)

    except (NotFoundUserError, NotVerifiedPasswordError) as error:
        raise IncorrectLoginOrPasswordError("Неправильный логин или пароль") from error

    return await _issue_tokens(
        device_id=uuid4(), user_id=authenticated_user.id, sessions_repository=sessions_repository
    )


async def logout(access_token: AccessToken, sessions_repository: ISessionsRepository) -> None:
    sessions = await sessions_repository.get_all_by_user_id_and_device_id_and_revoked(
        user_id=access_token.user_id, device_id=access_token.device_id, revoked=False
    )

    for session in sessions:
        session.revoke()

    await sessions_repository.update(*sessions)


async def refresh_tokens(
    refresh_token: RefreshToken, sessions_repository: ISessionsRepository
) -> tuple[AccessToken, RefreshToken]:
    """
    :raise AlreadySessionRevokedError: сессия отозвана
    """

    session = await sessions_repository.get_by_jti(jti=refresh_token.jti)

    try:
        session.revoke()
        await sessions_repository.update(session)

    except AlreadySessionRevokedError:
        non_revoked_sessions = await sessions_repository.get_all_by_user_id_and_revoked(
            user_id=session.user_id, revoked=False
        )

        for non_revoked_session in non_revoked_sessions:
            non_revoked_session.revoke()

        await sessions_repository.update(*non_revoked_sessions)
        raise

    return await _issue_tokens(
        device_id=session.device_id, user_id=session.user_id, sessions_repository=sessions_repository
    )


async def _issue_tokens(
    device_id: UUID, user_id: UUID, sessions_repository: ISessionsRepository
) -> tuple[AccessToken, RefreshToken]:
    refresh = RefreshToken(jti=uuid4(), device_id=device_id, user_id=user_id, iat=datetime.now(tz=timezone.utc))
    access = AccessToken(jti=uuid4(), device_id=device_id, user_id=user_id, iat=datetime.now(tz=timezone.utc))

    session = Session(
        id=uuid4(),
        jti=refresh.jti,
        user_id=user_id,
        device_id=device_id,
        revoked=False,
        created_at=datetime.now(tz=timezone.utc),
    )

    await sessions_repository.save(session)

    return access, refresh
