from datetime import date


from app.nutrition.commands.context import NutritionContext
from app.nutrition.commands.repositories import IPupilsRepository
from app.nutrition.domain.periods import CancellationPeriod
from app.nutrition.domain.pupil import PreferentialCertificate, Pupil
from app.nutrition.queries.dto import MealStatus
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.fastapi.schemas import FrontendModel
from app.shared.unit_of_work.abc import IUnitOfWork


class GetNutritionInfoQuery(Query):
    pupil_id: str


class MealPlanOut(FrontendModel):
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class PreferentialCertificateOut(FrontendModel):
    ends_at: date

    @classmethod
    def from_model(cls, certificate: PreferentialCertificate) -> "PreferentialCertificateOut":
        return cls(
            ends_at=certificate.ends_at,
        )


class CancellationPeriodOut(FrontendModel):
    starts_at: date
    ends_at: date
    reasons: list[str]

    @classmethod
    def from_model(cls, period: CancellationPeriod) -> "CancellationPeriodOut":
        return cls(
            starts_at=period.starts_at,
            ends_at=period.ends_at,
            reasons=[reason.value for reason in period.reasons],
        )


class NutritionOut(FrontendModel):
    id: str
    last_name: str
    first_name: str
    meal_plan: MealPlanOut
    preferential_certificate: PreferentialCertificateOut | None
    cancellation_periods: list[CancellationPeriodOut]
    status: MealStatus

    @classmethod
    def from_model(cls, pupil: Pupil) -> "NutritionOut":
        return cls(
            id=pupil.id.value,
            last_name=pupil.last_name.value,
            first_name=pupil.first_name.value,
            meal_plan=MealPlanOut(
                has_breakfast=pupil.has_breakfast, has_dinner=pupil.has_dinner, has_snacks=pupil.has_snacks
            ),
            preferential_certificate=PreferentialCertificateOut.from_model(pupil.preferential_certificate)
            if pupil.preferential_certificate
            else None,
            cancellation_periods=[CancellationPeriodOut.from_model(period) for period in pupil.cancellation_periods],
            status=MealStatus.from_model(pupil.nutrition_status),
        )


class GetNutritionInfoQueryExecutor(IQueryExecutor[GetNutritionInfoQuery, NutritionOut]):
    def __init__(self, pupils_repository: IPupilsRepository) -> None:
        self._pupils_repository = pupils_repository

    async def execute(self, query: GetNutritionInfoQuery) -> NutritionOut:
        """
        :raise NotFoundPupil: не найден ученик
        """

        return NutritionOut.from_model(pupil=await self._pupils_repository.get_by_id(pupil_id=query.pupil_id))
