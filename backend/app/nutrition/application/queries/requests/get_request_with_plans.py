from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.repositories import NotFoundDraftRequest, NotFoundRequest
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan, Name, Pupil
from app.nutrition.domain.school_class import SchoolClass
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.unit_of_work.abc import IUnitOfWork


class GetRequestWithPlansQuery(Query):
    class_id: UUID
    on_date: date


class RequestStatus(str, Enum):
    NOT_SUBMITTED = "Не подана"
    ON_EDITING = "На редактировании"
    SUBMITTED = "Подана"


class PupilWithPlanDTO(BaseModel):
    id: str
    last_name: str
    first_name: str
    patronymic: str | None
    breakfast: bool
    dinner: bool
    snacks: bool


class RequestWithPlansDTO(BaseModel):
    class_id: UUID
    on_date: date
    status: RequestStatus
    pupils: list[PupilWithPlanDTO]


class GetRequestWithPlansQueryExecutor(IQueryExecutor[GetRequestWithPlansQuery, RequestWithPlansDTO]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def execute(self, query: GetRequestWithPlansQuery) -> RequestWithPlansDTO:
        """
        :raise NotFoundSchoolClass: не найден класс по идентификатору
        """

        async with self._unit_of_work as context:
            school_class = await context.school_classes.get_by_id(id_=query.class_id)

            try:
                return await self._get_submitted(school_class, context, query)
            except NotFoundRequest:
                return await self._get_draft(school_class, context, query)

    async def _get_submitted(
        self, school_class: SchoolClass, context: NutritionContext, query: GetRequestWithPlansQuery
    ) -> RequestWithPlansDTO:
        request = await context.requests.get_by_class_id_and_date(class_id=query.class_id, on_date=Day(query.on_date))
        existent_pupils = {pupil.id: pupil for pupil in school_class.pupils}

        return RequestWithPlansDTO(
            class_id=school_class.id,
            on_date=request.on_date.date,
            status=RequestStatus.SUBMITTED,
            pupils=[
                PupilWithPlanDTO(
                    id=pupil.id.value,
                    last_name=existent_pupils[pupil.id].last_name.value,
                    first_name=existent_pupils[pupil.id].first_name.value,
                    patronymic=self._get_patronymic(existent_pupils[pupil.id].patronymic),
                    breakfast=pupil.plan.breakfast,
                    dinner=pupil.plan.dinner,
                    snacks=pupil.plan.snacks,
                )
                for pupil in request.pupils
                if pupil.id in existent_pupils
            ],
        )

    @staticmethod
    def _get_patronymic(name: Name | None) -> str | None:
        return name.value if name else None

    async def _get_draft(
        self, school_class: SchoolClass, context: NutritionContext, query: GetRequestWithPlansQuery
    ) -> RequestWithPlansDTO:
        pupils: list[PupilWithPlanDTO] = []

        try:
            draft = await context.draft_requests.get_by_class_id_and_date(
                class_id=query.class_id, on_date=Day(query.on_date)
            )

            for pupil in school_class.pupils:
                plan = draft.pupils.get(pupil.id) or self._prefill_plan(pupil, on_date=Day(query.on_date))
                pupils += [
                    PupilWithPlanDTO(
                        id=pupil.id.value,
                        last_name=pupil.last_name.value,
                        first_name=pupil.first_name.value,
                        patronymic=pupil.patronymic.value if pupil.patronymic else None,
                        breakfast=plan.breakfast,
                        dinner=plan.dinner,
                        snacks=plan.snacks,
                    )
                ]

            return RequestWithPlansDTO(
                class_id=school_class.id,
                on_date=draft.on_date.date,
                status=RequestStatus.ON_EDITING,
                pupils=pupils,
            )

        except NotFoundDraftRequest:
            for pupil in school_class.pupils:
                plan = self._prefill_plan(pupil, on_date=Day(query.on_date))
                pupils += [
                    PupilWithPlanDTO(
                        id=pupil.id.value,
                        last_name=pupil.last_name.value,
                        first_name=pupil.first_name.value,
                        patronymic=pupil.patronymic.value if pupil.patronymic else None,
                        breakfast=plan.breakfast,
                        dinner=plan.dinner,
                        snacks=plan.snacks,
                    )
                ]

            return RequestWithPlansDTO(
                class_id=school_class.id,
                on_date=query.on_date,
                status=RequestStatus.NOT_SUBMITTED,
                pupils=pupils,
            )

    @staticmethod
    def _prefill_plan(pupil: Pupil, on_date: Day) -> MealPlan:
        return (
            MealPlan(breakfast=False, dinner=False, snacks=False)
            if on_date in pupil.cancellation_periods
            else pupil.meal_plan
        )
