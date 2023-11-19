from enum import Enum

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.nutrition.domain.certificate import PreferentialCertificate
from app.nutrition.domain.meal_plan import MealPlan


class CantAttachExpiredPreferentialCertificate(Exception):
    pass


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
        if not self.meal_plan.is_feeding:
            return MealStatus.NONE

        if self.preferential_certificate and not self.preferential_certificate.is_expired:
            return MealStatus.PREFERENTIAL

        return MealStatus.PAID

    def update_meal_plan(self, plan: MealPlan) -> "Pupil":
        self.meal_plan = plan
        return self

    def attach_preferential_certificate(self, certificate: PreferentialCertificate) -> "Pupil":
        """
        :raise CantAddExpiredPreferentialCertificate: сертификат просрочен
        """

        if certificate.is_expired:
            raise CantAttachExpiredPreferentialCertificate

        self.preferential_certificate = certificate
        return self

    def detach_preferential_certificate(self) -> "Pupil":
        self.preferential_certificate = None
        return self
