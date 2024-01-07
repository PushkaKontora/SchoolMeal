from app.nutrition.application.context import NutritionContext
from app.nutrition.application.queries.dto import PupilOut
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.unit_of_work.abc import IUnitOfWork


class GetPupilByIDQuery(Query):
    pupil_id: str


class GetPupilByIDQueryExecutor(IQueryExecutor[GetPupilByIDQuery, PupilOut]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def execute(self, query: GetPupilByIDQuery) -> PupilOut:
        """
        :raise NotFoundPupil: не найден ученик
        """

        async with self._unit_of_work as context:
            pupil = await context.pupils.get_by_id(pupil_id=query.pupil_id)

            return PupilOut.from_model(pupil)
