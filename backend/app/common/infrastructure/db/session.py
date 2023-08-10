from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import database


Session = async_sessionmaker(
    bind=create_async_engine(url=database.dsn, pool_size=database.pool_size),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def session_with_transaction() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        async with session.begin():
            yield session
