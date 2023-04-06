from abc import ABC, abstractmethod
from typing import Type
from unittest.mock import Mock

import pytest
from dependency_injector.containers import DeclarativeContainer, override
from dependency_injector.providers import Factory

from app.database.container import DatabaseContainer
from app.database.unit_of_work import (
    IRepository,
    NotFoundRepositoryInterfaceException,
    RepositoryDependency,
    TransactionAlreadyBeganException,
    TransactionNotBeganException,
    TRepository,
    UnitOfWork,
)


class MockORMRepository(IRepository, ABC):
    pass


class IMockRepository(IRepository):
    @abstractmethod
    async def do_stuff(self) -> None:
        raise NotImplementedError


class INotInjectedRepository(IRepository):
    pass


class MockRepository(MockORMRepository, IMockRepository):
    async def do_stuff(self) -> None:
        pass


class MockUnitOfWork(UnitOfWork):
    def __init__(self, begin_mock: Mock, commit_mock: Mock, rollback_mock: Mock):
        super().__init__([RepositoryDependency(IMockRepository, MockRepository)])
        self.begin_mock = begin_mock
        self.commit_mock = commit_mock
        self.rollback_mock = rollback_mock

    async def _begin(self) -> None:
        self.begin_mock()

    async def _commit(self) -> None:
        self.commit_mock()

    async def _rollback(self) -> None:
        self.rollback_mock()

    def _get_repository(self, interface: Type[TRepository]) -> TRepository:
        return self._interfaces[interface]()


@override(DatabaseContainer)
class OverridingDatabaseContainer(DeclarativeContainer):
    begin_mock = Factory(Mock)
    commit_mock = Factory(Mock)
    rollback_mock = Factory(Mock)

    uow = Factory(MockUnitOfWork, begin_mock=begin_mock, commit_mock=commit_mock, rollback_mock=rollback_mock)


@pytest.fixture(scope="module")
def container() -> OverridingDatabaseContainer:
    return OverridingDatabaseContainer()


@pytest.fixture(scope="function")
def uow(container: OverridingDatabaseContainer) -> MockUnitOfWork:
    return container.uow()


@pytest.mark.unit
async def test_commit(uow: MockUnitOfWork):
    async with uow:
        await uow.commit()

    uow.commit_mock.assert_called_once()


@pytest.mark.unit
async def test_rollback(uow: MockUnitOfWork):
    async with uow:
        await uow.rollback()

    uow.rollback_mock.assert_called_once()


@pytest.mark.unit
async def test_begin(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.begin_mock.assert_called_once()


@pytest.mark.unit
async def test_disable_autocommit(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.commit_mock.assert_not_called()


@pytest.mark.unit
async def test_no_rollback_after_complete_transaction(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.rollback_mock.assert_not_called()


@pytest.mark.unit
async def test_be_rollback_after_interrupting_transaction(uow: MockUnitOfWork):
    class DomainException(Exception):
        pass

    try:
        async with uow:
            raise DomainException
    except DomainException:
        uow.rollback_mock.assert_called_once()
    else:
        raise Exception("__aexit__ covers exception")


@pytest.mark.unit
async def test_commit_not_began_transaction(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganException):
        await uow.commit()


@pytest.mark.unit
async def test_rollback_not_began_transaction(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganException):
        await uow.rollback()


@pytest.mark.unit
async def test_begin_transaction_that_already_began(uow: MockUnitOfWork):
    with pytest.raises(TransactionAlreadyBeganException):
        async with uow:
            async with uow:
                pass


@pytest.mark.unit
async def test_get_repository_by_interface(uow: MockUnitOfWork):
    async with uow:
        actual = uow.get_repository(IMockRepository)
        assert type(actual) is MockRepository


@pytest.mark.unit
async def test_throw_exception_if_interface_is_not_injected_to_uow(uow: MockUnitOfWork):
    with pytest.raises(NotFoundRepositoryInterfaceException):
        async with uow:
            uow.get_repository(INotInjectedRepository)


@pytest.mark.unit
async def test_throw_exception_if_transaction_has_not_began_yet(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganException):
        uow.get_repository(IMockRepository)
