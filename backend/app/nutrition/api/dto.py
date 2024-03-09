from datetime import date
from enum import Enum
from typing import Any, Callable
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.application.dao.pupils import PupilByIDs
from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import NutritionStatus, Pupil
from app.nutrition.domain.time import Period
from app.shared.api.dto import Filters
from app.shared.domain.pupil import PupilID
from app.shared.specifications import Specification


class MealtimeDTO(str, Enum):
    BREAKFAST = "breakfast"
    DINNER = "dinner"
    SNACKS = "snacks"

    def to_model(self) -> Mealtime:
        return {
            self.BREAKFAST: Mealtime.BREAKFAST,
            self.DINNER: Mealtime.DINNER,
            self.SNACKS: Mealtime.SNACKS,
        }[self]

    @classmethod
    def from_model(cls, mealtime: Mealtime) -> "MealtimeDTO":
        return {
            Mealtime.BREAKFAST: cls.BREAKFAST,
            Mealtime.DINNER: cls.DINNER,
            Mealtime.SNACKS: cls.SNACKS,
        }[mealtime]


class NutritionStatusOut(str, Enum):
    PAID = "paid"
    PREFERENTIAL = "preferential"

    @classmethod
    def from_model(cls, status: NutritionStatus) -> "NutritionStatusOut":
        return {
            NutritionStatus.PAID: cls.PAID,
            NutritionStatus.PREFERENTIAL: cls.PREFERENTIAL,
        }[status]


class ResumedPupilIn(BaseModel):
    id: str
    mealtimes: set[MealtimeDTO]

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResumedPupilIn) and self.id == other.id


class PupilFilters(Filters[Pupil]):
    ids: set[str] | None = None

    def _build_map(self) -> dict[str, Callable[[Any], Specification[Pupil]]]:
        return {
            "ids": lambda x: PupilByIDs({PupilID(pupil_id) for pupil_id in x}),
        }


class PeriodOut(BaseModel):
    start: date
    end: date

    @classmethod
    def from_model(cls, period: Period) -> "PeriodOut":
        return cls(start=period.start, end=period.end)


class PupilOut(BaseModel):
    id: str
    class_id: UUID
    mealtimes: set[MealtimeDTO]
    preferential_until: date | None
    cancelled_periods: list[PeriodOut]
    nutrition: NutritionStatusOut

    @classmethod
    def from_model(cls, pupil: Pupil) -> "PupilOut":
        return cls(
            id=pupil.id.value,
            class_id=pupil.class_id.value,
            mealtimes={MealtimeDTO.from_model(mealtime) for mealtime in pupil.mealtimes},
            preferential_until=pupil.preferential_until,
            cancelled_periods=[PeriodOut.from_model(period) for period in pupil.cancelled_periods],
            nutrition=NutritionStatusOut.from_model(pupil.nutrition),
        )
