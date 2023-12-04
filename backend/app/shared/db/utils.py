from asyncio import sleep

from asyncpg import InvalidCatalogNameError
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.shared.db.settings import DatabaseSettings


async def exists_database(settings: DatabaseSettings) -> bool:
    try:
        engine = create_async_engine(settings.url)
        async with engine.connect():
            return True
    except InvalidCatalogNameError:
        return False


async def wait_connect(settings: DatabaseSettings) -> None:
    engine = create_async_engine(settings.url)

    while True:
        try:
            logger.info(f"Подключение к БД {settings}")
            async with engine.connect():
                logger.success("Подключение к БД установлено")
                return

        except InvalidCatalogNameError:
            logger.success("Подключение к БД установлено, но отсутствует БД")
            return

        except Exception as error:
            logger.error(f"Не удалось подключиться к БД {settings} - {error}")

        await sleep(10)


async def create_database(settings: DatabaseSettings) -> None:
    query = f"CREATE DATABASE {settings.database}"

    logger.info(f"Создание базы {settings.database}")

    engine = create_async_engine(DatabaseSettings(database="postgres").url, isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(query))

    logger.success(f"База {settings.database} успешно создана")
