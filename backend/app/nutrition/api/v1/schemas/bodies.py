from datetime import date
from uuid import UUID

from app.nutrition.api.v1.schemas.enums import MealtimeDTO
from app.shared.api.schemas import FrontendBody


class ResumedPupilIn(FrontendBody):
    id: str
    mealtimes: set[MealtimeDTO]

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResumedPupilIn) and self.id == other.id


class SubmitRequestBody(FrontendBody):
    class_id: UUID
    on_date: date
    overrides: set[ResumedPupilIn]


class ResumePupilOnDayBody(FrontendBody):
    day: date


class CancelPupilForPeriodBody(FrontendBody):
    start: date
    end: date
    reason: str | None


class UpdateMealtimesBody(FrontendBody):
    mealtimes: dict[MealtimeDTO, bool]
