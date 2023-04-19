from abc import ABC
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.database.specifications import FilterSpecification


class Base(DeclarativeBase):
    pass


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

    async def find_one(self, specification: FilterSpecification) -> T:
        query = specification(select(self.model).limit(1))

        return await self.session.scalar(query)

    async def find(self, specification: FilterSpecification) -> list[T]:
        query = specification(select(self.model))

        return list(await self.session.scalars(query))

    async def exists(self, specification: FilterSpecification) -> bool:
        return bool(await self.find_one(specification))
