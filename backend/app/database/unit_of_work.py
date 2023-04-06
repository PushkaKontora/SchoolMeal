from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, Type, TypeVar


class IRepository:
    pass


TRepository = TypeVar("TRepository", bound=IRepository)
TRepositoryImplementation = TypeVar("TRepositoryImplementation")


@dataclass
class RepositoryDependency(Generic[TRepositoryImplementation]):
    interface: Type[IRepository]
    implementation: Type[TRepositoryImplementation]


class UnitOfWork(Generic[TRepositoryImplementation], ABC):
    def __init__(self, repositories: Iterable[RepositoryDependency]):
        self._is_began = False
        self._interfaces: dict[Type[IRepository], Type[TRepositoryImplementation]] = {
            d.interface: d.implementation for d in repositories
        }

    async def commit(self) -> None:
        if not self._is_began:
            raise TransactionNotBeganException

        await self._commit()

    async def rollback(self) -> None:
        if not self._is_began:
            raise TransactionNotBeganException

        await self._rollback()

    def get_repository(self, interface: Type[TRepository]) -> TRepository:
        if not self._is_began:
            raise TransactionNotBeganException

        if interface not in self._interfaces:
            raise NotFoundRepositoryInterfaceException

        return self._get_repository(interface)

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
    def _get_repository(self, interface: Type[TRepository]) -> TRepository:
        raise NotImplementedError

    async def _begin_transaction(self) -> None:
        if self._is_began:
            raise TransactionAlreadyBeganException

        self._is_began = True
        await self._begin()

    async def __aenter__(self):
        await self._begin_transaction()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()

        self._is_began = False


class TransactionAlreadyBeganException(Exception):
    pass


class TransactionNotBeganException(Exception):
    pass


class NotFoundRepositoryInterfaceException(Exception):
    pass
