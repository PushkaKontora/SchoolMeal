from dataclasses import replace
from types import TracebackType
from typing import Callable, TypeVar

from app.shared.unit_of_work.abc import IUnitOfWork, TContext, UnitOfWorkHasNotBeenOpenedYet


T = TypeVar("T")


# TODO: убрать
class UnitOfWorkIsAlreadyOpened(Exception):
    pass


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
