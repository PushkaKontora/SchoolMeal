from uuid import UUID

from app.account.application.repositories import (
    ICredentialsRepository,
    ISessionsRepository,
    IUsersRepository,
    NotFoundCredentialError,
    NotFoundSessionError,
    NotUniqueLoginError,
)
from app.account.domain.credential import Credential
from app.account.domain.login import Login
from app.account.domain.session import Session
from app.account.domain.user import User


class LocalCredentialsRepository(ICredentialsRepository):
    def __init__(self, credentials: list[Credential] | None = None) -> None:
        self._credentials = credentials or []

    async def get_by_login(self, login: Login) -> Credential:
        try:
            return next(cred for cred in self._credentials if cred.login == login)
        except StopIteration as error:
            raise NotFoundCredentialError from error


class LocalSessionsRepository(ISessionsRepository):
    def __init__(self) -> None:
        self._sessions: dict[UUID, Session] = {}

    async def save(self, *sessions: Session) -> None:
        self._sessions |= {session.id: session for session in sessions}

    async def update(self, *sessions: Session) -> None:
        await self.save(*sessions)

    async def get_by_jti(self, jti: UUID) -> Session:
        try:
            return next(session for session in self._sessions.values() if session.jti == jti)
        except StopIteration as error:
            raise NotFoundSessionError from error

    async def get_all_by_credential_id_and_revoked(self, credential_id: UUID, revoked: bool) -> list[Session]:
        return [
            session
            for session in self._sessions.values()
            if session.credential_id == credential_id and session.revoked == revoked
        ]

    async def get_all_by_credential_id_and_device_id_and_revoked(
        self, credential_id: UUID, device_id: UUID, revoked: bool
    ) -> list[Session]:
        return [
            session
            for session in self._sessions.values()
            if session.credential_id == credential_id and session.device_id == device_id and session.revoked == revoked
        ]


class LocalUsersRepository(IUsersRepository):
    def __init__(self, users: list[User] | None = None) -> None:
        self._users = users or []

    async def save(self, user: User) -> None:
        if any(saved_user for saved_user in self._users if saved_user.credential.login == user.credential.login):
            raise NotUniqueLoginError

        self._users += [user]
