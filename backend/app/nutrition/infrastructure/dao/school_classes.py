from typing import AsyncContextManager, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao.school_classes import Filter, ISchoolClassRepository
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.infrastructure.db import SchoolClassDB


class AlchemySchoolClassRepository(ISchoolClassRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get(self, ident: ClassID) -> SchoolClass | None:
        async with self._session_factory() as session:
            class_db = await session.get(SchoolClassDB, ident=ident.value)

            return class_db.to_model() if class_db else None

    async def all(self, spec: Filter | None = None) -> list[SchoolClass]:
        query = select(SchoolClassDB)

        async with self._session_factory() as session:
            classes = (class_db.to_model() for class_db in (await session.scalars(query)).all())

            return list(filter(lambda x: spec.is_satisfied_by(x), classes) if spec else classes)
