from abc import ABC, abstractmethod
from unittest.mock import Mock

import pytest
from dependency_injector.containers import DeclarativeContainer, override
from dependency_injector.providers import Factory

from app.database.container import Database
from app.database.unit_of_work import TransactionAlreadyBeganError, TransactionNotBeganError, UnitOfWork


pytestmark = [pytest.mark.unit]


class IMockRepository(ABC):
    @abstractmethod
    async def do_stuff(self) -> None:
        raise NotImplementedError


class MockRepository(IMockRepository):
    async def do_stuff(self) -> None:
        pass


class MockUnitOfWork(UnitOfWork):
    repository = UnitOfWork.Repository()

    def __init__(self, begin_mock: Mock, commit_mock: Mock, rollback_mock: Mock, close_mock: Mock):
        super().__init__()
        self.begin_mock = begin_mock
        self.commit_mock = commit_mock
        self.rollback_mock = rollback_mock
        self.close_mock = close_mock

    async def _begin(self) -> None:
        self.begin_mock()
        self.repository = Mock()

    async def _commit(self) -> None:
        self.commit_mock()

    async def _rollback(self) -> None:
        self.rollback_mock()

    async def _close(self) -> None:
        self.close_mock()


@override(Database)
class OverridingDatabaseContainer(DeclarativeContainer):
    begin_mock = Factory(Mock)
    commit_mock = Factory(Mock)
    rollback_mock = Factory(Mock)
    close_mock = Factory(Mock)

    uow = Factory(
        MockUnitOfWork,
        begin_mock=begin_mock,
        commit_mock=commit_mock,
        rollback_mock=rollback_mock,
        close_mock=close_mock,
    )


@pytest.fixture(scope="module")
def container() -> OverridingDatabaseContainer:
    return OverridingDatabaseContainer()


@pytest.fixture(scope="function")
def uow(container: OverridingDatabaseContainer) -> MockUnitOfWork:
    return container.uow()


async def test_commit(uow: MockUnitOfWork):
    async with uow:
        await uow.commit()

    uow.commit_mock.assert_called_once()


async def test_rollback(uow: MockUnitOfWork):
    async with uow:
        await uow.rollback()

    uow.rollback_mock.assert_called_once()


async def test_begin_and_close(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.begin_mock.assert_called_once()
    uow.close_mock.assert_called_once()


async def test_disable_autocommit(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.commit_mock.assert_not_called()


async def test_no_rollback_after_complete_transaction(uow: MockUnitOfWork):
    async with uow:
        pass

    uow.rollback_mock.assert_not_called()


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


async def test_commit_not_began_transaction(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganError):
        await uow.commit()


async def test_rollback_not_began_transaction(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganError):
        await uow.rollback()


async def test_begin_transaction_that_already_began(uow: MockUnitOfWork):
    with pytest.raises(TransactionAlreadyBeganError):
        async with uow:
            async with uow:
                pass


async def test_correct_getting_repository(uow: MockUnitOfWork):
    async with uow:
        repo1, repo2 = uow.repository, uow.repository
        assert repo1 is repo2

    async with uow:
        repo3 = uow.repository
        assert repo3 is not repo1


async def test_getting_repository_from_not_began_uow(uow: MockUnitOfWork):
    with pytest.raises(TransactionNotBeganError):
        uow.repository
