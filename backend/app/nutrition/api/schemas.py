from datetime import date
from enum import Enum

from app.common.api.schemas import FrontendModel
from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriod
from app.nutrition.domain.pupil import MealStatus, Pupil


class MealPlanIn(FrontendModel):
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class MealPlanOut(MealPlanIn):
    @classmethod
    def from_model(cls, plan: MealPlan) -> "MealPlanOut":
        return cls(
            has_breakfast=plan.has_breakfast,
            has_dinner=plan.has_dinner,
            has_snacks=plan.has_snacks,
        )


class PreferentialCertificateOut(FrontendModel):
    ends_at: date

    @classmethod
    def from_model(cls, certificate: PreferentialCertificate) -> "PreferentialCertificateOut":
        return cls(
            ends_at=certificate.ends_at,
        )


class CancellationPeriodIn(FrontendModel):
    starts_at: date
    ends_at: date
    reason: str | None


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


class MealStatusOut(str, Enum):
    PREFERENTIAL = "Льготное питание"
    PAID = "Платное питание"
    NONE = "Не питается"

    @classmethod
    def from_model(cls, status: MealStatus) -> "MealStatusOut":
        mapper = {MealStatus.PREFERENTIAL: cls.PREFERENTIAL, MealStatus.PAID: cls.PAID, MealStatus.NONE: cls.NONE}
        return mapper[status]


class NutritionOut(FrontendModel):
    id: str
    last_name: str
    first_name: str
    meal_plan: MealPlanOut
    preferential_certificate: PreferentialCertificateOut | None
    cancellation_periods: list[CancellationPeriodOut]
    status: MealStatusOut

    @classmethod
    def from_model(cls, pupil: Pupil) -> "NutritionOut":
        return cls(
            id=pupil.id.value,
            last_name=pupil.last_name.value,
            first_name=pupil.first_name.value,
            meal_plan=MealPlanOut.from_model(pupil.meal_plan),
            preferential_certificate=PreferentialCertificateOut.from_model(pupil.preferential_certificate)
            if pupil.preferential_certificate
            else None,
            cancellation_periods=[CancellationPeriodOut.from_model(period) for period in pupil.cancellation_periods],
            status=MealStatusOut.from_model(pupil.status),
        )
