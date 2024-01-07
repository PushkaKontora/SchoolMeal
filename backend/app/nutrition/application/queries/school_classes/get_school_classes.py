from uuid import UUID

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.queries.dto import SchoolClassOut
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.unit_of_work.abc import IUnitOfWork


class GetSchoolClassesQuery(Query):
    teacher_id: UUID


class GetSchoolClassesQueryExecutor(IQueryExecutor[GetSchoolClassesQuery, list[SchoolClassOut]]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def execute(self, query: GetSchoolClassesQuery) -> list[SchoolClassOut]:
        async with self._unit_of_work as context:
            school_classes = await context.school_classes.get_all_by_teacher_id(teacher_id=query.teacher_id)

            return [SchoolClassOut.from_model(school_class) for school_class in school_classes]
