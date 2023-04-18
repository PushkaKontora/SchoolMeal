from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.auth.db.repositories import IssuedTokensRepository, PasswordsRepository
from app.config import DatabaseSettings
from app.database.unit_of_work import UnitOfWork
from app.users.db.repositories import UsersRepository


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(url=settings.dsn)


class Database(DeclarativeContainer):
    settings = Singleton(DatabaseSettings)

    engine = Callable(create_engine, settings)
    session_maker = Singleton(async_sessionmaker[AsyncSession], bind=engine)

    unit_of_work = Factory(
        UnitOfWork,
        session_maker=session_maker,
        users_repository=UsersRepository,
        passwords_repository=PasswordsRepository,
        issued_tokens_repository=IssuedTokensRepository,
    )
