import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.database import Session, engine
from app.main import app


@pytest.fixture(scope="session")
async def connection() -> AsyncConnection:
    async with engine.connect() as connection:
        yield connection


@pytest.fixture(scope="function")
async def session(connection: AsyncConnection) -> AsyncSession:
    Session.configure(bind=connection)
    main_transaction = await connection.begin()

    session = Session()
    session.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    try:
        yield session
    finally:
        await main_transaction.rollback()


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
