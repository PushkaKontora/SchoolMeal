from typing import Callable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.nutrition.application.queries.dto import MealStatus
from app.nutrition.infrastructure.db.models import PupilDB, SchoolClassDB, SchoolDB
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.fastapi.schemas import FrontendModel


class GetChildrenQuery(Query):
    parent_id: UUID


class School(FrontendModel):
    id: UUID
    name: str

    @classmethod
    def from_db(cls, school_db: SchoolDB) -> "School":
        return cls(
            id=school_db.id,
            name=school_db.name,
        )


class SchoolClass(FrontendModel):
    id: UUID
    school: School
    number: int
    literal: str

    @classmethod
    def from_db(cls, school_class_db: SchoolClassDB) -> "SchoolClass":
        return cls(
            id=school_class_db.id,
            school=School.from_db(school_class_db.school),
            number=school_class_db.number,
            literal=school_class_db.literal,
        )


class MealPlan(FrontendModel):
    status: MealStatus


class ChildOut(FrontendModel):
    id: str
    last_name: str
    first_name: str
    school_class: SchoolClass
    meal_plan: MealPlan

    @classmethod
    def from_db(cls, pupil_db: PupilDB) -> "ChildOut":
        return cls(
            id=pupil_db.id,
            last_name=pupil_db.last_name,
            first_name=pupil_db.first_name,
            school_class=SchoolClass.from_db(pupil_db.school_class),
            meal_plan=MealPlan(status=MealStatus.from_model(pupil_db.to_model().nutrition_status)),
        )


class GetChildrenQueryExecutor(IQueryExecutor[GetChildrenQuery, list[ChildOut]]):
    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        self._session_factory = session_factory

    async def execute(self, query: GetChildrenQuery) -> list[ChildOut]:
        async with self._session_factory() as session:
            pupils_db: list[PupilDB] = (
                await session.scalars(
                    select(PupilDB)
                    .join(PupilDB.parents)
                    .where(PupilDB.parents.any(id=query.parent_id))
                    .options(joinedload(PupilDB.school_class))
                    .options(joinedload(PupilDB.school_class).joinedload(SchoolClassDB.school))
                    .options(selectinload(PupilDB.cancellation_periods))
                )
            ).all()

            return [ChildOut.from_db(pupil_db) for pupil_db in pupils_db]
