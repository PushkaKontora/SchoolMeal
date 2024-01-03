from types import TracebackType
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.unit_of_work.abc import IUnitOfWork, TContext, UnitOfWorkHasNotBeenOpenedYet, UnitOfWorkIsAlreadyOpened


class AlchemyUnitOfWork(IUnitOfWork[TContext]):
    def __init__(
        self, session_factory: Callable[[], AsyncSession], context_factory: Callable[[AsyncSession], TContext]
    ) -> None:
        self._context_factory = context_factory
        self._session_factory = session_factory

        self._session: AsyncSession | None = None

    async def __aenter__(self) -> TContext:
        if self._session:
            raise UnitOfWorkIsAlreadyOpened

        self._session = await self._session_factory().__aenter__()
        await self._session.begin()

        return self._context_factory(self._session)

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        await self._session.__aexit__(exc_type, exc_value, traceback)

    async def commit(self) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        await self._session.commit()

    async def rollback(self) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        await self._session.rollback()
