from uuid import UUID

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.queries.dto import PupilOut
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.unit_of_work.abc import IUnitOfWork


class GetPupilsQuery(Query):
    class_id: UUID


class GetPupilsQueryExecutor(IQueryExecutor[GetPupilsQuery, list[PupilOut]]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def execute(self, query: GetPupilsQuery) -> list[PupilOut]:
        async with self._unit_of_work as context:
            pupils = await context.pupils.get_by_class_id(class_id=query.class_id)

            return [PupilOut.from_model(pupil) for pupil in pupils]
