import secrets
from dataclasses import field
from datetime import date, datetime
from enum import Enum

from pydantic.dataclasses import dataclass

from app.nutrition.domain.periods import CancellationPeriod, CancellationPeriodSequence, Day
from app.shared.domain import timezones
from app.shared.domain.abc import Entity, ValueObject


class CantAttachExpiredPreferentialCertificate(Exception):
    pass


class CannotCancelNutritionAfterTime(Exception):
    def __init__(self, now: datetime, completed_at: datetime) -> None:
        self.now = now
        self.completed_at = completed_at


class CannotResumeNutritionAfterTime(Exception):
    def __init__(self, now: datetime, completed_at: datetime) -> None:
        self.now = now
        self.completed_at = completed_at


@dataclass(eq=True, frozen=True)
class PupilID(ValueObject):
    value: str = field(default_factory=lambda: secrets.token_hex(10))


@dataclass(eq=True, frozen=True)
class Name(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class PreferentialCertificate(ValueObject):
    ends_at: date

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezones.yekaterinburg).date() > self.ends_at


class NutritionStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


@dataclass
class MealPlan:
    breakfast: bool
    dinner: bool
    snacks: bool


@dataclass
class Pupil(Entity):
    id: PupilID
    first_name: Name
    last_name: Name
    patronymic: Name | None
    meal_plan: MealPlan
    preferential_certificate: PreferentialCertificate | None
    cancellation_periods: CancellationPeriodSequence

    @property
    def nutrition_status(self) -> NutritionStatus:
        if not any([self.meal_plan.breakfast, self.meal_plan.dinner, self.meal_plan.snacks]):
            return NutritionStatus.NONE

        if self.is_preferential:
            return NutritionStatus.PREFERENTIAL

        return NutritionStatus.PAID

    @property
    def is_preferential(self) -> bool:
        return self.preferential_certificate is not None and not self.preferential_certificate.is_expired

    def update_meal_plan(self, meal_plan: MealPlan) -> None:
        self.meal_plan = meal_plan

    def cancel_nutrition(self, period: CancellationPeriod) -> None:
        """
        :raise CannotCancelNutritionAfterTime: нельзя снимать с питания после 10 утра по ЕКБ
        """

        now = datetime.now(timezones.yekaterinburg)
        if now.hour > 10 and now.date() in period:
            raise CannotCancelNutritionAfterTime(
                now=now, completed_at=now.replace(hour=10, minute=0, second=0, microsecond=0)
            )

        self.cancellation_periods = self.cancellation_periods.insert(period)

    def resume_nutrition(self, day: Day) -> None:
        """
        :raise CannotResumeNutritionAfterTime: нельзя ставить на питание после 10 утра по ЕКБ
        """

        now = datetime.now(timezones.yekaterinburg)
        if now.hour > 10 and now.date() in day:
            raise CannotResumeNutritionAfterTime(
                now=now, completed_at=now.replace(hour=10, minute=0, second=0, microsecond=0)
            )

        self.cancellation_periods = self.cancellation_periods.remove(day)
