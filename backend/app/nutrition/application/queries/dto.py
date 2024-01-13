from datetime import date
from enum import Enum
from uuid import UUID

from app.nutrition.application.dto import CancellationPeriodOut
from app.nutrition.domain.pupil import NutritionStatus, PreferentialCertificate, Pupil
from app.nutrition.domain.school_class import SchoolClass, SchoolClassInitials
from app.shared.fastapi.schemas import FrontendModel


class MealStatus(str, Enum):
    PREFERENTIAL = "Питается льготно"
    PAID = "Питается платно"
    NONE = "Не питается"

    @classmethod
    def from_model(cls, status: NutritionStatus) -> "MealStatus":
        mapper = {
            NutritionStatus.PREFERENTIAL: cls.PREFERENTIAL,
            NutritionStatus.PAID: cls.PAID,
            NutritionStatus.NONE: cls.NONE,
        }
        return mapper[status]


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


class PupilOut(FrontendModel):
    id: str
    last_name: str
    first_name: str
    meal_plan: MealPlanOut
    preferential_certificate: PreferentialCertificateOut | None
    cancellation_periods: list[CancellationPeriodOut]
    status: MealStatus

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilOut":
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


class InitialsOut(FrontendModel):
    literal: str
    number: int

    @classmethod
    def from_model(cls, initials: SchoolClassInitials) -> "InitialsOut":
        return cls(
            literal=initials.literal,
            number=initials.number,
        )


class SchoolClassOut(FrontendModel):
    id: UUID
    initials: InitialsOut
    breakfast: bool
    dinner: bool
    snacks: bool

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassOut":
        return cls(
            id=school_class.id,
            initials=InitialsOut.from_model(school_class.initials),
            breakfast=school_class.breakfast,
            dinner=school_class.dinner,
            snacks=school_class.snacks,
        )


class FoodOut(FrontendModel):
    id: UUID
    name: str
    description: str
    calories: str
    proteins: str
    fats: str
    carbohydrates: str
    weight: str
    price: str
    photo_url: str | None


class MealtimeInfo(FrontendModel):
    foods: list[FoodOut]
    cost: str


class MenuOut(FrontendModel):
    id: UUID
    on_date: date
    breakfast: MealtimeInfo
    dinner: MealtimeInfo
    snacks: MealtimeInfo
