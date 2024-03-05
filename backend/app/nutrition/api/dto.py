from datetime import date
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.domain.mealtime import Mealtime


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


class ResumePupilOnDayIn(BaseModel):
    pupil_id: str
    day: date


class CancelPupilForPeriodIn(BaseModel):
    pupil_id: str
    start: date
    end: date


class UpdateMealtimesAtPupilIn(BaseModel):
    pupil_id: str
    mealtimes: dict[MealtimeDTO, bool]


class ResumedPupilIn(BaseModel):
    id: str
    mealtimes: set[MealtimeDTO]

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResumedPupilIn) and self.id == other.id


class SubmitRequestToCanteenIn(BaseModel):
    class_id: UUID
    on_date: date
    overrides: set[ResumedPupilIn]


class AttachPupilToParentIn(BaseModel):
    parent_id: UUID
    pupil_id: str
