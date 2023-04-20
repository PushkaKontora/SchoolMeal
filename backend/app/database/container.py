from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.auth.db.repositories import IssuedTokensRepository, PasswordsRepository
from app.config import DatabaseSettings
from app.database.unit_of_work import UnitOfWork
from app.users.db.models import User
from app.users.db.repositories import UsersRepository
from app.users.domain.base_repositories import BaseUsersRepository


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(url=settings.dsn)


def create_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
    return session_maker()


class Database(DeclarativeContainer):
    settings = Singleton(DatabaseSettings)

    engine = Callable(create_engine, settings)
    session_maker = Singleton(async_sessionmaker[AsyncSession], bind=engine)
    session = Callable(create_session, session_maker=session_maker)

    users_repository: Factory[BaseUsersRepository] = Factory(UsersRepository, session=session, model=User)

    unit_of_work = Factory(
        UnitOfWork,
        session=session,
        users_repository=UsersRepository,
        passwords_repository=PasswordsRepository,
        issued_tokens_repository=IssuedTokensRepository,
    )
