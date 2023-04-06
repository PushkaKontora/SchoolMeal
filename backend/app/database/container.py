from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import DatabaseSettings
from app.database.sqlalchemy import AlchemyUnitOfWork


class DatabaseContainer(DeclarativeContainer):
    config = Configuration(pydantic_settings=[DatabaseSettings()])

    engine = Singleton(create_async_engine, url=config.dsn)
    session_maker = Singleton(async_sessionmaker, bind=engine)

    uow = Factory(AlchemyUnitOfWork, session_maker=session_maker)
