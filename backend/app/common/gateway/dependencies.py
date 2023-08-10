from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.infrastructure.db.session import Session


async def get_db_session() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        yield session
