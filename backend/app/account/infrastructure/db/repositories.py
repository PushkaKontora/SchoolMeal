from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.account.infrastructure.db.models import CredentialDB, SessionDB, UserDB


class CredentialsRepository(ICredentialsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_login(self, login: Login) -> Credential:
        try:
            query = select(CredentialDB).where(CredentialDB.login == login.value)
            user_db: CredentialDB = (await self._session.scalars(query)).one()

            return user_db.to_model()

        except NoResultFound as error:
            raise NotFoundCredentialError from error


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

    async def get_all_by_credential_id_and_revoked(self, credential_id: UUID, revoked: bool) -> list[Session]:
        query = select(SessionDB).where(SessionDB.credential_id == credential_id, SessionDB.revoked == revoked)
        sessions_db: list[SessionDB] = (await self._session.scalars(query)).all()

        return [session_db.to_model() for session_db in sessions_db]

    async def get_all_by_credential_id_and_device_id_and_revoked(
        self, credential_id: UUID, device_id: UUID, revoked: bool
    ) -> list[Session]:
        query = select(SessionDB).where(
            SessionDB.credential_id == credential_id, SessionDB.device_id == device_id, SessionDB.revoked == revoked
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

                await self._session.flush([user_db.credential, user_db])

        except IntegrityError as error:
            raise NotUniqueLoginError from error
