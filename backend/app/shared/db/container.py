from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Callable, Configuration, Factory, Singleton
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class DatabaseContainer(DeclarativeContainer):
    database_config = Configuration(strict=True)
    alchemy_config = Configuration(strict=True)

    database_url = Callable(
        URL.create,
        drivername=database_config.driver,
        username=database_config.user,
        password=database_config.password,
        host=database_config.host,
        port=database_config.port,
        database=database_config.database,
    )

    engine = Singleton(
        create_async_engine,
        url=database_url,
        echo=alchemy_config.echo,
        pool_size=alchemy_config.pool_size,
    )

    session = Factory(
        AsyncSession,
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
