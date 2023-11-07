from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.infrastructure.db.session import Session


async def _get_session() -> AsyncIterator[AsyncSession]:
    async with Session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(_get_session)]
