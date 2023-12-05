from uuid import UUID

from app.users.application.repositories import (
    ISessionsRepository,
    IUsersRepository,
    NotFoundSession,
    NotFoundUser,
    NotUniqueLogin,
)
from app.users.domain.login import Login
from app.users.domain.session import Session
from app.users.domain.user import User


class LocalSessionsRepository(ISessionsRepository):
    def __init__(self) -> None:
        self._sessions: dict[UUID, Session] = {}

    async def save(self, *sessions: Session) -> None:
        self._sessions |= {session.id: session for session in sessions}

    async def update(self, session: Session) -> None:
        await self.save(session)

    async def get_by_jti(self, jti: UUID) -> Session:
        try:
            return next(session for session in self._sessions.values() if session.jti == jti)
        except StopIteration as error:
            raise NotFoundSession from error

    async def get_all_by_user_id_and_revoked(self, user_id: UUID, revoked: bool) -> list[Session]:
        return [
            session for session in self._sessions.values() if session.user_id == user_id and session.revoked == revoked
        ]

    async def get_all_by_user_id_and_device_id_and_revoked(
        self, user_id: UUID, device_id: UUID, revoked: bool
    ) -> list[Session]:
        return [
            session
            for session in self._sessions.values()
            if session.user_id == user_id and session.device_id == device_id and session.revoked == revoked
        ]


class LocalUsersRepository(IUsersRepository):
    def __init__(self, users: list[User] | None = None) -> None:
        self._users = users or []

    async def save(self, user: User) -> None:
        if any(saved_user for saved_user in self._users if saved_user.login == user.login):
            raise NotUniqueLogin

        self._users += [user]

    async def get_by_login(self, login: Login) -> User:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration as error:
            raise NotFoundUser from error

    async def get_by_id(self, user_id: UUID) -> User:
        try:
            return next(user for user in self._users if user.id == user_id)
        except StopIteration as error:
            raise NotFoundUser from error
