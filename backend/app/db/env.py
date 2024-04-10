import asyncio

from alembic import context
from alembic.context import config
from sqlalchemy import MetaData, pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.orm import DeclarativeBase

from app.db.settings import DatabaseSettings
from app.db.utils import create_database, exists_database, wait_connect
from app.feedbacks.infrastructure.db import FeedbacksBase
from app.notification.infrastructure.db import NotificationBase
from app.nutrition.infrastructure.db import NutritionBase
from app.user_management.infrastructure.db import UserManagementBase


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


database = DatabaseSettings()

SCHEMAS: list[type[DeclarativeBase]] = [
    NutritionBase,
    FeedbacksBase,
    UserManagementBase,
    NotificationBase,
]
target_metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

for schema in SCHEMAS:
    for table in schema.metadata.tables.values():
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


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}) | {"sqlalchemy.url": database.url},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    await wait_connect(database)

    if not await exists_database(database):
        await create_database(database)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


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


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
