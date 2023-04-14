from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.auth.db.sqlalchemy.repositories import AlchemyIssuedTokensRepository, AlchemyPasswordsRepository
from app.config import DatabaseSettings
from app.database.sqlalchemy.unit_of_work import AlchemyUnitOfWork
from app.users.db.sqlalchemy.repositories import AlchemyUsersRepository


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(url=settings.dsn)


class Database(DeclarativeContainer):
    settings = Singleton(DatabaseSettings)

    engine = Callable(create_engine, settings)
    session_maker = Singleton(async_sessionmaker[AsyncSession], bind=engine)

    unit_of_work = Factory(
        AlchemyUnitOfWork,
        session_maker=session_maker,
        users_repository=AlchemyUsersRepository,
        passwords_repository=AlchemyPasswordsRepository,
        issued_tokens_repository=AlchemyIssuedTokensRepository,
    )
