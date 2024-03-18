from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.api.v1.schemas.enums import MealtimeDTO


class ResumedPupilIn(BaseModel):
    id: str
    mealtimes: set[MealtimeDTO]

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResumedPupilIn) and self.id == other.id


class SubmitRequestBody(BaseModel):
    class_id: UUID
    on_date: date
    overrides: set[ResumedPupilIn]


class ResumePupilOnDayBody(BaseModel):
    day: date


class CancelPupilForPeriodBody(BaseModel):
    start: date
    end: date
    reason: str | None


class UpdateMealtimesBody(BaseModel):
    mealtimes: dict[MealtimeDTO, bool]
