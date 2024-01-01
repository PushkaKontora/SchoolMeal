from enum import Enum

from pydantic.dataclasses import dataclass

from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriod, CancellationPeriodSequence, Day
from app.shared.domain import Entity, ValueObject


class CantAttachExpiredPreferentialCertificate(Exception):
    pass


@dataclass(eq=True, frozen=True)
class PupilID(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class FirstName(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class LastName(ValueObject):
    value: str


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


@dataclass
class Pupil(Entity):
    id: PupilID
    last_name: LastName
    first_name: FirstName
    meal_plan: MealPlan
    preferential_certificate: PreferentialCertificate | None
    cancellation_periods: CancellationPeriodSequence

    @property
    def status(self) -> MealStatus:
        if not self.meal_plan.is_feeding:
            return MealStatus.NONE

        if self.preferential_certificate and not self.preferential_certificate.is_expired:
            return MealStatus.PREFERENTIAL

        return MealStatus.PAID

    def update_meal_plan(self, plan: MealPlan) -> None:
        self.meal_plan = plan

    def attach_preferential_certificate(self, certificate: PreferentialCertificate) -> None:
        """
        :raise CantAddExpiredPreferentialCertificate: сертификат просрочен
        """

        if certificate.is_expired:
            raise CantAttachExpiredPreferentialCertificate

        self.preferential_certificate = certificate

    def detach_preferential_certificate(self) -> None:
        self.preferential_certificate = None

    def cancel_nutrition(self, period: CancellationPeriod) -> CancellationPeriodSequence:
        self.cancellation_periods = self.cancellation_periods.insert(period)
        return self.cancellation_periods

    def resume_nutrition(self, day: Day) -> CancellationPeriodSequence:
        self.cancellation_periods = self.cancellation_periods.remove(day)
        return self.cancellation_periods
