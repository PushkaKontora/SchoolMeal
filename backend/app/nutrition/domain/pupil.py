import secrets
from dataclasses import field
from datetime import date, datetime, timezone
from enum import Enum

from pydantic.dataclasses import dataclass

from app.nutrition.domain.periods import CancellationPeriod, CancellationPeriodSequence, Day
from app.shared.domain import Entity, ValueObject


class CantAttachExpiredPreferentialCertificate(Exception):
    pass


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
        return datetime.now(timezone.utc).date() > self.ends_at


class NutritionStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


@dataclass
class Pupil(Entity):
    id: PupilID
    first_name: Name
    last_name: Name
    patronymic: Name | None
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool
    preferential_certificate: PreferentialCertificate | None
    cancellation_periods: CancellationPeriodSequence

    @property
    def nutrition_status(self) -> NutritionStatus:
        if not any([self.has_breakfast, self.has_dinner, self.has_snacks]):
            return NutritionStatus.NONE

        if self.preferential_certificate and not self.preferential_certificate.is_expired:
            return NutritionStatus.PREFERENTIAL

        return NutritionStatus.PAID

    def update_mealtimes(self, has_breakfast: bool, has_dinner: bool, has_snacks: bool) -> None:
        self.has_breakfast = has_breakfast
        self.has_dinner = has_dinner
        self.has_snacks = has_snacks

    def cancel_nutrition(self, period: CancellationPeriod) -> None:
        self.cancellation_periods = self.cancellation_periods.insert(period)

    def resume_nutrition(self, day: Day) -> None:
        self.cancellation_periods = self.cancellation_periods.remove(day)
