from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.unit_of_work import UnitOfWork
from app.users.db.sqlalchemy.repositories import AlchemyUsersRepository


class AlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_maker: async_sessionmaker[AsyncSession], users_repository: Type[AlchemyUsersRepository]):
        super().__init__()

        self._session_maker = session_maker
        self._users_repository = users_repository

    async def _begin(self) -> None:
        self._session = self._session_maker()

        self.users_repository = self._users_repository(self._session)

    async def _commit(self) -> None:
        await self._session.commit()

    async def _rollback(self) -> None:
        await self._session.rollback()

    async def _close(self) -> None:
        await self._session.close()
