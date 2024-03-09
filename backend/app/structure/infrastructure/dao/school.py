from typing import AsyncContextManager, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.structure.application.dao.school import ISchoolDAO
from app.structure.domain.school import School
from app.structure.infrastructure.db import SchoolDB


class AlchemySchoolDAO(ISchoolDAO):
    def __init__(self, session_factory: Callable[[], AsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get(self) -> School:
        async with self._session_factory() as session:
            school_db = await session.get(SchoolDB, ident=1)

            if not school_db:
                raise RuntimeError("Не заполнены данные о школе")

            return school_db.to_model()
