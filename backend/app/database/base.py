from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy import MetaData, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.database.specifications import Specification


POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


T = TypeVar("T", bound=Base)


class Repository(Generic[T], ABC):
    model: type[T]

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    def save(self, obj: T) -> None:
        self.session.add(obj)

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)

    def update(self, obj: T) -> None:
        self.session.add(obj)

    async def refresh(self, obj: T) -> None:
        await self.session.refresh(obj)

    async def all(self) -> list[T]:
        query = select(self.model)

        return list(await self.session.scalars(query))

    async def find_one(self, *specifications: Specification) -> T | None:
        query = select(self.model).limit(1)

        for spec in specifications:
            query = spec(query)

        return await self.session.scalar(query)

    async def find(self, *specifications: Specification) -> list[T]:
        query = select(self.model)

        for spec in specifications:
            query = spec(query)

        return list(await self.session.scalars(query))

    async def exists(self, *specifications: Specification) -> bool:
        return bool(await self.find_one(*specifications))
