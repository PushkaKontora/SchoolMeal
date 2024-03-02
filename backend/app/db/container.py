from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


class AlchemyORM(DeclarativeContainer):
    config = providers.Configuration(strict=True)

    url = providers.Callable(
        URL.create,
        drivername=config.driver,
        username=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database,
    )

    engine = providers.Singleton(
        create_async_engine,
        url=url,
        echo=config.echo,
        pool_size=config.pool_size,
    )

    session = providers.Factory(
        AsyncSession,
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
