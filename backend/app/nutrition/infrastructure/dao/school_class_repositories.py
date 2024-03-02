from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.application.dao import ISchoolClassRepository
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.infrastructure.db import SchoolClassDB


class AlchemySchoolClassRepository(ISchoolClassRepository):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, id_: ClassID) -> SchoolClass | None:
        async with self._session_factory() as session:
            class_db = await session.get(SchoolClassDB, ident=id_.value)

            return class_db.to_model() if class_db else None
