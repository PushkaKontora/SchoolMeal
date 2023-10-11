from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Callable, Configuration, Dependency, Factory, Singleton
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.config import AppSettings, CORSSettings, DatabaseSettings, JWTSettings, PasswordSettings, S3StorageSettings
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.utils.storages import LocalStorage, S3Storage, Storage


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(url=settings.dsn)


def create_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncSession:
    return session_maker()


class AppContainer(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    app_settings = Singleton(AppSettings)
    cors_settings = Singleton(CORSSettings)
    database_settings = Singleton(DatabaseSettings)
    jwt_settings = Singleton(JWTSettings)
    password_settings = Singleton(PasswordSettings)

    engine = Callable(create_engine, database_settings)
    session_maker = Singleton(async_sessionmaker[AsyncSession], bind=engine)
    session = Callable(create_session, session_maker)
    unit_of_work = Factory(UnitOfWork, session=session)

    storage = Dependency(instance_of=Storage)


class S3StorageContainer(DeclarativeContainer):
    storage_settings = Configuration(pydantic_settings=[S3StorageSettings()])
    storage = Singleton(
        S3Storage,
        access_key=storage_settings.access_key,
        secret_key=storage_settings.secret_key,
        endpoint=storage_settings.endpoint,
        bucket_name=storage_settings.bucket_name,
        url_ttl=storage_settings.presigned_url_ttl,
    )


class LocalStorageContainer(DeclarativeContainer):
    storage = Singleton(LocalStorage, endpoint="http://localhost/media")