from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, declarative_base


CASCADE = "CASCADE"


Base: DeclarativeMeta = declarative_base()


class AlchemyRepository(ABC):
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session
