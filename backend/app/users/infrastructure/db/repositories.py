from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.application.repositories import (
    ISessionsRepository,
    IUsersRepository,
    NotFoundSessionError,
    NotFoundUserError,
    NotUniqueLoginError,
)
from app.users.domain.login import Login
from app.users.domain.session import Session
from app.users.domain.user import User
from app.users.infrastructure.db.models import SessionDB, UserDB


class SessionsRepository(ISessionsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, *sessions: Session) -> None:
        sessions_db = list(map(SessionDB.from_model, sessions))

        for session_db in sessions_db:
            self._session.add(session_db)

        await self._session.flush(sessions_db)

    async def update(self, *sessions: Session) -> None:
        for session_db in map(SessionDB.from_model, sessions):
            query = update(SessionDB).values(session_db.dict()).where(SessionDB.id == session_db.id)
            await self._session.execute(query)

    async def get_by_jti(self, jti: UUID) -> Session:
        try:
            query = select(SessionDB).where(SessionDB.jti == jti)
            session_db: SessionDB = (await self._session.scalars(query)).one()

        except NoResultFound as error:
            raise NotFoundSessionError from error

        return session_db.to_model()

    async def get_all_by_user_id_and_revoked(self, user_id: UUID, revoked: bool) -> list[Session]:
        query = select(SessionDB).where(SessionDB.user_id == user_id, SessionDB.revoked == revoked)
        sessions_db: list[SessionDB] = (await self._session.scalars(query)).all()

        return [session_db.to_model() for session_db in sessions_db]

    async def get_all_by_user_id_and_device_id_and_revoked(
        self, user_id: UUID, device_id: UUID, revoked: bool
    ) -> list[Session]:
        query = select(SessionDB).where(
            SessionDB.user_id == user_id, SessionDB.device_id == device_id, SessionDB.revoked == revoked
        )
        sessions_db: list[SessionDB] = (await self._session.scalars(query)).all()

        return [session_db.to_model() for session_db in sessions_db]


class UsersRepository(IUsersRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, user: User) -> None:
        try:
            async with self._session.begin_nested():
                user_db = UserDB.from_model(user)
                self._session.add(user_db)
                await self._session.flush([user_db])

        except IntegrityError as error:
            raise NotUniqueLoginError from error

    async def get_by_login(self, login: Login) -> User:
        try:
            query = select(UserDB).where(UserDB.login == login.value)
            user_db: UserDB = (await self._session.scalars(query)).one()

        except NoResultFound as error:
            raise NotFoundUserError from error

        return user_db.to_model()

    async def get_by_id(self, user_id: UUID) -> User:
        try:
            query = select(UserDB).where(UserDB.id == user_id)
            user_db: UserDB = (await self._session.scalars(query)).one()

        except NoResultFound as error:
            raise NotFoundUserError from error

        return user_db.to_model()
