from abc import ABC

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import DatabaseSettings


CASCADE = "CASCADE"


class Base(DeclarativeBase):
    pass


class AlchemyRepository(ABC):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(settings.dsn)
