from typing import AsyncContextManager, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.specifications import Specification
from app.structure.application.dao.school_classes import ISchoolClassRepository
from app.structure.domain.school_class import SchoolClass
from app.structure.infrastructure.db import SchoolClassDB


class AlchemySchoolClassRepository(ISchoolClassRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def all(self, spec: Specification[SchoolClass] | None = None) -> list[SchoolClass]:
        query = select(SchoolClassDB)

        async with self._session_factory() as session:
            classes = (class_db.to_model() for class_db in (await session.scalars(query)).all())

            return list(filter(lambda x: spec.is_satisfied_by(x), classes) if spec else classes)
