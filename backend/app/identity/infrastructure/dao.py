from datetime import datetime
from typing import AsyncContextManager, Callable
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.identity.application.dao import ISessionRepository, IUserRepository
from app.identity.domain.credentials import Login
from app.identity.domain.jwt import Session
from app.identity.domain.user import User
from app.identity.infrastructure.db import SessionDB, UserDB
from app.shared.domain.user import UserID


class AlchemyUserRepository(IUserRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, id_: UserID) -> User | None:
        async with self._session_factory() as session:
            user_db = await session.get(UserDB, ident=id_.value)

            return user_db.to_model() if user_db else None

    async def get_by_login(self, login: Login) -> User | None:
        query = select(UserDB).where(UserDB.login == login.value).limit(1)

        async with self._session_factory() as session:
            user_db = (await session.scalars(query)).one_or_none()

            return user_db.to_model() if user_db else None


class AlchemySessionRepository(ISessionRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def add(self, session: Session) -> None:
        session_db = SessionDB.from_model(session)

        async with self._session_factory() as alchemy_session:
            alchemy_session.add(session_db)
            await alchemy_session.commit()

    async def pop(self, id_: UUID) -> Session | None:
        query = delete(SessionDB).where(SessionDB.id == id_).returning(SessionDB)

        async with self._session_factory() as session:
            session_db = (await session.scalars(query)).one_or_none()
            await session.commit()

            return session_db.to_model() if session_db else None

    async def count_by_user_id(self, user_id: UserID) -> int:
        query = select(count(SessionDB.id)).where(SessionDB.user_id == user_id.value)

        async with self._session_factory() as session:
            return int(await session.scalar(query))

    async def remove_all_by_user_id(self, user_id: UserID) -> None:
        query = delete(SessionDB).where(SessionDB.user_id == user_id.value)

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()

    async def delete_all_expired(self, beginning_with: datetime) -> None:
        query = delete(SessionDB).where(SessionDB.expires_in >= beginning_with)

        async with self._session_factory() as session:
            await session.execute(query)
            await session.commit()
