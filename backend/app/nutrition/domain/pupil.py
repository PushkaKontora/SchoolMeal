from enum import Enum

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan


@dataclass(eq=True, frozen=True)
class PupilID:
    value: str


@dataclass(eq=True, frozen=True)
class FirstName:
    value: str


@dataclass(eq=True, frozen=True)
class LastName:
    value: str


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


class Pupil(BaseModel):
    id: PupilID
    last_name: LastName
    first_name: FirstName
    meal_plan: MealPlan
    preferential_certificate: PreferentialCertificate | None

    @property
    def status(self) -> MealStatus:
        if self.preferential_certificate and not self.preferential_certificate.is_ended:
            return MealStatus.PREFERENTIAL

        if not any(self.meal_plan.as_tuple()):
            return MealStatus.NONE

        return MealStatus.PAID
