import asyncio

import pytest
from dependency_injector.providers import Object
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.config import DatabaseSettings, JWTSettings
from app.container import AppContainer
from app.database.container import DatabaseContainer
from app.database.sqlalchemy.models import Base


@pytest.fixture(scope="session")
def container() -> AppContainer:
    return AppContainer()


@pytest.fixture(scope="session")
def db_container(container: AppContainer) -> DatabaseContainer:
    return container.database_container()


@pytest.fixture(scope="session")
def db_settings() -> DatabaseSettings:
    return DatabaseSettings(database="test_db")


@pytest.fixture(scope="session")
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture(scope="session")
async def connection(
    container: AppContainer, db_container: DatabaseContainer, db_settings: DatabaseSettings
) -> AsyncConnection:
    container.database_settings.override(Object(db_settings))
    engine = db_container.engine()

    async with engine.connect() as conn:
        db_container.engine.override(Object(conn))
        db_container.session_maker.reset()

        yield conn


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(container: AppContainer, connection: AsyncConnection):
    await connection.run_sync(Base.metadata.create_all)
    await connection.commit()

    yield

    await connection.run_sync(Base.metadata.drop_all)
    await connection.commit()


@pytest.fixture(scope="function")
async def session(db_container: DatabaseContainer, connection: AsyncConnection) -> AsyncSession:
    session_maker = db_container.session_maker()

    transaction = await connection.begin()
    nested = await connection.begin_nested()

    session = session_maker(expire_on_commit=False, autoflush=False)

    @event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(session, transaction):
        nonlocal nested

        if not nested.is_active:
            nested = connection.sync_connection.begin_nested()

    try:
        yield session
    finally:
        await transaction.rollback()
        await session.close()


@pytest.fixture(scope="session")
async def client(container: AppContainer) -> AsyncClient:
    async with AsyncClient(app=container.app(), base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()
