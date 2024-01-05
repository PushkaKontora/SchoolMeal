from typing import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.nutrition.infrastructure.db.models import SchoolClassDB
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.fastapi.schemas import FrontendModel


class GetSchoolClassesQuery(Query):
    teacher_id: UUID


class SchoolClassOut(FrontendModel):
    id: UUID
    number: int
    literal: str

    @classmethod
    def from_db(cls, school_class_db: SchoolClassDB) -> "SchoolClassOut":
        return cls(
            id=school_class_db.id,
            number=school_class_db.number,
            literal=school_class_db.literal,
        )


class GetSchoolClassesQueryExecutor(IQueryExecutor[GetSchoolClassesQuery, list[SchoolClassOut]]):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def execute(self, query: GetSchoolClassesQuery) -> list[SchoolClassOut]:
        async with self._session_factory() as session:
            query_db = (
                select(SchoolClassDB)
                .where(SchoolClassDB.teacher_id == query.teacher_id)
                .order_by(SchoolClassDB.number, SchoolClassDB.literal)
            )
            school_classes_db: list[SchoolClassDB] = (await session.scalars(query_db)).all()

            return [SchoolClassOut.from_db(school_class_db) for school_class_db in school_classes_db]
