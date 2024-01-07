from collections import deque
from types import TracebackType
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from app.shared.unit_of_work.abc import IUnitOfWork, TContext, UnitOfWorkHasNotBeenOpenedYet


class AlchemyUnitOfWork(IUnitOfWork[TContext]):
    def __init__(
        self, session_factory: Callable[[], AsyncSession], context_factory: Callable[[AsyncSession], TContext]
    ) -> None:
        self._context_factory = context_factory
        self._session_factory = session_factory

        self._session: AsyncSession | None = None
        self._transactions: deque[AsyncSessionTransaction] = deque()

    async def __aenter__(self) -> TContext:
        if not self._session:
            self._session = await self._session_factory().__aenter__()
            self._transactions.append(await self._session.begin())
        else:
            self._transactions.append(await self._session.begin_nested())

        return self._context_factory(self._session)

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        transaction = self._transactions.pop()
        await transaction.__aexit__(exc_type, exc_value, traceback)

        if not self._transactions:
            await self._session.__aexit__(exc_type, exc_value, traceback)
            self._session = None

    async def commit(self) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        await self._transactions[-1].commit()

    async def rollback(self) -> None:
        if not self._session:
            raise UnitOfWorkHasNotBeenOpenedYet

        await self._transactions[-1].commit()
