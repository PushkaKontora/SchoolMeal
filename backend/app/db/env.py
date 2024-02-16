import asyncio

from alembic import context
from alembic.config import Config
from sqlalchemy import MetaData, engine_from_config, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from app.feedbacks.infrastructure.db.models import FeedbacksBase
from app.nutrition.infrastructure.db.models import NutritionBase
from app.shared.db.settings import DatabaseSettings
from app.shared.db.utils import create_database, exists_database, wait_connect


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


database = DatabaseSettings()


config: Config = context.config
config.set_main_option("sqlalchemy.url", database.url)

bases = [NutritionBase, FeedbacksBase]
target_metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

for base in bases:
    for table in base.metadata.tables.values():
        table.to_metadata(target_metadata)


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
    context.configure(
        connection=connection,
        compare_type=True,
        target_metadata=target_metadata,
        version_table_schema=target_metadata.schema,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section)

    connectable = AsyncEngine(
        engine_from_config(
            configuration,
            poolclass=pool.NullPool,
            future=True,
        )  # type: ignore
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
