from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton, Object
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import DatabaseSettings
from app.database.sqlalchemy.unit_of_work import AlchemyUnitOfWork
from app.users.db.sqlalchemy.repositories import AlchemyUsersRepository


class DatabaseContainer(DeclarativeContainer):
    config = Configuration(pydantic_settings=[DatabaseSettings()])

    engine = Singleton(create_async_engine, url=config.dsn)
    session_maker = Singleton(async_sessionmaker, bind=engine)

    users_repository = Object(AlchemyUsersRepository)

    unit_of_work = Factory(AlchemyUnitOfWork, session_maker=session_maker, users_repository=users_repository)
