import asyncio

import pytest
from dependency_injector.containers import DeclarativeContainer, override
from dependency_injector.providers import Object
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database.container import DatabaseContainer
from app.database.sqlalchemy import AlchemyUnitOfWork
from app.database.unit_of_work import UnitOfWork
from app.main import app


class TestingUnitOfWork(AlchemyUnitOfWork):
    async def _begin(self) -> None:
        self._session = self._session_maker()

        await self._session.begin_nested()


@pytest.fixture(scope="session")
async def connection() -> AsyncConnection:
    container = DatabaseContainer()

    async with container.engine().connect() as connection:

        @override(DatabaseContainer)
        class OverridingDatabaseContainer(DeclarativeContainer):
            engine = Object(connection)

        yield connection


@pytest.fixture(scope="function")
async def uow(connection: AsyncConnection) -> UnitOfWork:
    container = DatabaseContainer()
    transaction = await connection.begin()

    try:
        async with TestingUnitOfWork(container.session_maker()) as uow:
            yield uow
    finally:
        await transaction.rollback()


@pytest.fixture(scope="session")
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()
