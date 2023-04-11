from abc import ABC
from typing import Iterable, Type

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from app.database.unit_of_work import IRepository, RepositoryDependency, TRepository, UnitOfWork


Base: DeclarativeMeta = declarative_base()

CASCADE = "CASCADE"


class AlchemyRepository(IRepository, ABC):
    def __init__(self, session: AsyncSession):
        self._session = session


class AlchemyUnitOfWork(UnitOfWork[AlchemyRepository]):
    def __init__(
        self,
        session_maker: async_sessionmaker[AsyncSession],
        repositories: Iterable[RepositoryDependency[AlchemyRepository]],
    ):
        super().__init__(repositories)

        self._session_maker = session_maker

    async def _begin(self) -> None:
        self._session = self._session_maker()

    async def _commit(self) -> None:
        await self._session.commit()

    async def _rollback(self) -> None:
        await self._session.rollback()

    def _get_repository(self, interface: Type[TRepository]) -> TRepository:
        return self._interfaces[interface](self._session)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)

        await self._session.close()
