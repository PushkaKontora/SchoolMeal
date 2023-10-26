from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository, NotFoundCredentialError
from app.account.domain.credential import IncorrectPasswordError
from app.account.domain.login import Login
from app.account.domain.passwords import Password
from app.account.domain.session import AlreadySessionRevokedError, Session
from app.account.domain.tokens import AccessToken, RefreshToken


class IncorrectLoginOrPasswordError(Exception):
    pass


async def authenticate(
    login: Login,
    password: Password,
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
) -> tuple[AccessToken, RefreshToken]:
    """
    :raise IncorrectLoginOrPasswordError: неправильный логин или пароль
    """

    try:
        credential = await credentials_repository.get_by_login(login)

        authenticated = credential.authenticate(password)

    except (NotFoundCredentialError, IncorrectPasswordError) as error:
        raise IncorrectLoginOrPasswordError("Неправильный логин или пароль") from error

    return await _issue_tokens(
        device_id=uuid4(), credential_id=authenticated.id, sessions_repository=sessions_repository
    )


async def logout(access: AccessToken, sessions_repository: ISessionsRepository) -> None:
    sessions = await sessions_repository.get_all_by_credential_id_and_device_id_and_revoked(
        credential_id=access.credential_id, device_id=access.device_id, revoked=False
    )

    for session in sessions:
        session.revoke()

    await sessions_repository.update(*sessions)


async def refresh_tokens(
    refresh: RefreshToken, sessions_repository: ISessionsRepository
) -> tuple[AccessToken, RefreshToken]:
    """
    :raise AlreadySessionRevokedError: сессия отозвана
    """

    session = await sessions_repository.get_by_jti(jti=refresh.jti)

    try:
        session.revoke()
        await sessions_repository.update(session)

    except AlreadySessionRevokedError:
        non_revoked_sessions = await sessions_repository.get_all_by_credential_id_and_revoked(
            credential_id=session.credential_id, revoked=False
        )

        for non_revoked_session in non_revoked_sessions:
            non_revoked_session.revoke()

        await sessions_repository.update(*non_revoked_sessions)
        raise

    return await _issue_tokens(
        device_id=session.device_id, credential_id=session.credential_id, sessions_repository=sessions_repository
    )


async def _issue_tokens(
    device_id: UUID, credential_id: UUID, sessions_repository: ISessionsRepository
) -> tuple[AccessToken, RefreshToken]:
    refresh = RefreshToken(
        jti=uuid4(), device_id=device_id, credential_id=credential_id, iat=datetime.now(tz=timezone.utc)
    )
    access = AccessToken(
        jti=uuid4(), device_id=device_id, credential_id=credential_id, iat=datetime.now(tz=timezone.utc)
    )

    session = Session(
        id=uuid4(),
        jti=refresh.jti,
        credential_id=credential_id,
        device_id=device_id,
        revoked=False,
        created_at=datetime.now(tz=timezone.utc),
    )

    await sessions_repository.save(session)

    return access, refresh
