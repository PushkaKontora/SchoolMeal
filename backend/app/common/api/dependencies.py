from typing import Annotated, AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.infrastructure.db.session import get_session_cls
from app.common.infrastructure.settings import DatabaseSettings


def _get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


def _get_session_cls(
    settings: DatabaseSettings = Depends(_get_database_settings, use_cache=True)
) -> type[AsyncSession]:
    return get_session_cls(settings)


async def _get_session(
    session_cls: type[AsyncSession] = Depends(_get_session_cls, use_cache=True)
) -> AsyncIterator[AsyncSession]:
    async with session_cls() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(_get_session)]
