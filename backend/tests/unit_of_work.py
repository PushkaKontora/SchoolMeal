from dataclasses import replace
from types import TracebackType
from typing import Callable, TypeVar

from app.shared.unit_of_work.abc import (
    ISavepoint,
    ISavepointManager,
    IUnitOfWork,
    TContext,
    UnitOfWorkHasNotBeenOpenedYet,
    UnitOfWorkIsAlreadyOpened,
)


T = TypeVar("T")


class LocalUnitOfWork(IUnitOfWork[TContext]):
    def __init__(self, context_factory: Callable[[], TContext]) -> None:
        self._context_factory = context_factory

        self._previous_context: TContext | None = None
        self._context: TContext | None = None

        self._temp_context: TContext | None = None

    async def commit(self) -> None:
        if not self._temp_context:
            raise UnitOfWorkHasNotBeenOpenedYet

        self._context = self._temp_context
        self._temp_context = None

    async def rollback(self) -> None:
        if not self._temp_context:
            raise UnitOfWorkHasNotBeenOpenedYet

        self._context = self._previous_context
        self._temp_context = None

    async def __aenter__(self) -> TContext:
        if self._temp_context:
            raise UnitOfWorkIsAlreadyOpened

        self._previous_context = self._context
        self._temp_context = replace(self._context) if self._context else self._context_factory()

        return self._temp_context

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        if self._temp_context and exc_value:
            await self.rollback()

        self._temp_context = None

    def begin_savepoint(self) -> ISavepointManager:
        if not self._temp_context:
            raise UnitOfWorkHasNotBeenOpenedYet

        def _update(context: TContext) -> None:
            self._temp_context = context

        return _LocalSavepointManager(replace(self._temp_context), _update)


class _LocalSavepointManager(ISavepointManager):
    def __init__(self, context: TContext, update: Callable[[TContext], None]) -> None:
        self._context = context
        self._update = update

    async def __aenter__(self) -> ISavepoint:
        return _LocalSavepoint(self._context, self._update)

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None
    ) -> None:
        pass


class _LocalSavepoint(ISavepoint):
    def __init__(self, context: TContext, update: Callable[[TContext], None]) -> None:
        self._context = context
        self._update = update

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        self._update(self._context)
