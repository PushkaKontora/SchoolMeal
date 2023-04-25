import asyncio

import pytest
from dependency_injector.providers import Object
from fastapi import FastAPI
from httpx import AsyncClient, Auth, Request
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from app.config import DatabaseSettings, JWTSettings
from app.database.base import Base
from app.database.container import Database
from app.main import create_app
from app.users.db.models import Role, User
from tests.auth.integration.conftest import create_access_token


class BearerAuth(Auth):
    def __init__(self, token: str):
        self._token = token

    def auth_flow(self, request: Request):
        request.headers["Authorization"] = f"Bearer {self._token}"

        yield request


@pytest.fixture
async def parent(session: AsyncSession) -> User:
    user = User(
        last_name="Dykov",
        first_name="Lima",
        login="abc",
        role=Role.PARENT,
        phone="+78005553535",
        email="email@email.com",
        photo_path=r"https://yandex.ru/images/",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
async def teacher(session: AsyncSession) -> User:
    user = User(
        last_name="Samkov",
        first_name="Nikita",
        login="qwersvasdf",
        role=Role.TEACHER,
        phone="+79999999999",
        email="asdfqwer@email.com",
        photo_path=r"https://yandex.ru/images/qwfdvxzcv",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest.fixture
def parent_token(parent: User, jwt_settings: JWTSettings) -> str:
    return create_access_token(parent.id, parent.role, jwt_settings)


@pytest.fixture(scope="session")
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture(scope="session")
async def connection() -> AsyncConnection:
    Database.settings.override(DatabaseSettings(database="test_db"))
    engine = Database.engine()

    async with engine.connect() as conn:
        Database.engine.override(Object(conn))
        Database.session_maker.reset()

        yield conn


@pytest.fixture(scope="session", autouse=True)
async def prepare_database(connection: AsyncConnection):
    await connection.run_sync(Base.metadata.create_all)
    await connection.commit()

    yield

    await connection.run_sync(Base.metadata.drop_all)
    await connection.commit()


@pytest.fixture(scope="function")
async def session(connection: AsyncConnection) -> AsyncSession:
    session_maker = Database.session_maker()

    transaction = await connection.begin()
    session = session_maker(expire_on_commit=False, autoflush=False, bind=connection)

    nested = await connection.begin_nested()

    @event.listens_for(session.sync_session, "after_transaction_end")
    def end_savepoint(session_, transaction_):
        nonlocal nested

        if not nested.is_active:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        await transaction.rollback()
        await session.close()


@pytest.fixture(scope="session")
def app_() -> FastAPI:
    return create_app()


@pytest.fixture
async def client(app_: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app_, base_url="http://localhost") as client:
        yield client


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()

    yield loop

    loop.close()
