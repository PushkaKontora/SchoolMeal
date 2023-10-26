import asyncio

from alembic import context
from alembic.config import Config
from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from app.common.infrastructure.db.base import Base
from app.common.infrastructure.db.utils import create_database, exists_database, wait_connect
from app.common.infrastructure.settings import database


from app.users.infrastructure.db.models import SessionDB, UserDB  # isort: skip


config: Config = context.config
config.set_main_option("sqlalchemy.url", database.url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=database.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)

    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            poolclass=pool.NullPool,
            future=True,
        )
    )

    await wait_connect(database)

    if not await exists_database(database):
        await create_database(database)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
