from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Callable, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import AppSettings, DatabaseSettings, JWTSettings, PasswordSettings, RequestSignatureSettings
from app.db.unit_of_work import UnitOfWork


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(url=settings.dsn, echo=True)


def create_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
    return session_maker()


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    app_settings = Singleton(AppSettings)
    database_settings = Singleton(DatabaseSettings)
    jwt_settings = Singleton(JWTSettings)
    password_settings = Singleton(PasswordSettings)
    request_signature_settings = Singleton(RequestSignatureSettings)

    engine = Callable(create_engine, database_settings)
    session_maker = Singleton(async_sessionmaker[AsyncSession], bind=engine)
    session = Callable(create_session, session_maker)
    unit_of_work = Factory(UnitOfWork, session=session)
