from datetime import date
from enum import Enum
from typing import Callable
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.application.context import NutritionContext
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan
from app.nutrition.domain.request import Request
from app.nutrition.domain.school_class import SchoolClass, SchoolClassType
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.unit_of_work.abc import IUnitOfWork


class ClassType(str, Enum):
    PRIMARY = "primary"
    HIGH = "high"

    def to_model(self) -> SchoolClassType:
        return {
            self.PRIMARY: SchoolClassType.PRIMARY,
            self.HIGH: SchoolClassType.HIGH,
        }[self]


class GetCountedRequestsQuery(Query):
    class_type: ClassType
    on_date: date


class Meal(BaseModel):
    paid: int
    preferential: int
    total: int

    @classmethod
    def default(cls) -> "Meal":
        return cls(
            paid=0,
            preferential=0,
            total=0,
        )


class ClassReport(BaseModel):
    id: UUID
    initials: str
    breakfast: Meal
    dinner: Meal
    snacks: Meal


class Report(BaseModel):
    school_classes: list[ClassReport]
    paid_total: int
    preferential_total: int
    total: int


class GetCountedRequestsQueryExecutor(IQueryExecutor[GetCountedRequestsQuery, Report]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def execute(self, query: GetCountedRequestsQuery) -> Report:
        async with self._unit_of_work as context:
            school_classes = await context.school_classes.get_all_by_type(class_type=query.class_type.to_model())
            requests = {
                request.class_id: request
                for request in await context.requests.get_all_by_date(on_date=Day(query.on_date))
            }

            reports = [self._prepare_class_report(school_class, requests) for school_class in school_classes]
            paid_total = sum(report.breakfast.paid + report.dinner.paid + report.snacks.paid for report in reports)
            preferential_total = sum(
                report.breakfast.preferential + report.dinner.preferential + report.snacks.preferential
                for report in reports
            )

            return Report(
                school_classes=reports,
                paid_total=paid_total,
                preferential_total=preferential_total,
                total=paid_total + preferential_total,
            )

    def _prepare_class_report(self, school_class: SchoolClass, requests: dict[UUID, Request]) -> ClassReport:
        request = requests.get(school_class.id)

        if not request:
            return ClassReport(
                id=school_class.id,
                initials=str(school_class.initials),
                breakfast=Meal.default(),
                dinner=Meal.default(),
                snacks=Meal.default(),
            )

        return ClassReport(
            id=school_class.id,
            initials=str(school_class.initials),
            breakfast=self._prepare_request_report(lambda plan: plan.breakfast, request),
            dinner=self._prepare_request_report(lambda plan: plan.dinner, request),
            snacks=self._prepare_request_report(lambda plan: plan.snacks, request),
        )

    @staticmethod
    def _prepare_request_report(mealtime: Callable[[MealPlan], bool], request: Request) -> Meal:
        paid = sum(int(mealtime(pupil.plan) and not pupil.preferential) for pupil in request.pupils)
        preferential = sum(int(mealtime(pupil.plan) and pupil.preferential) for pupil in request.pupils)

        return Meal(paid=paid, preferential=preferential, total=paid + preferential)
