from abc import ABC, abstractmethod
from typing import Type

from app.users.domain.repositories import IUsersRepository


class UnitOfWork(ABC):
    class Repository:
        def __set_name__(self, owner: Type["UnitOfWork"], name: str):
            self.name = f"_{name}"

        def __get__(self, instance: "UnitOfWork", owner: Type["UnitOfWork"]):
            if not instance._is_began:
                raise TransactionNotBeganError

            return getattr(instance, self.name)

    def __init__(self):
        self._is_began = False

    async def commit(self) -> None:
        if not self._is_began:
            raise TransactionNotBeganError

        await self._commit()

    async def rollback(self) -> None:
        if not self._is_began:
            raise TransactionNotBeganError

        await self._rollback()

    async def _begin_transaction(self) -> None:
        if self._is_began:
            raise TransactionAlreadyBeganError

        self._is_began = True

        await self._begin()

    async def __aenter__(self):
        await self._begin_transaction()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

        self._is_began = False
        await self._close()

    @abstractmethod
    async def _begin(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _rollback(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def _close(self) -> None:
        raise NotImplementedError


class TransactionAlreadyBeganError(Exception):
    pass


class TransactionNotBeganError(Exception):
    pass
