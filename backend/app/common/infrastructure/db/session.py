from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.common.infrastructure.settings import DatabaseSettings


def get_session_cls(settings: DatabaseSettings) -> type[AsyncSession]:
    return sessionmaker(  # type: ignore
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
        bind=create_async_engine(url=settings.url, pool_size=settings.pool_size),
    )
