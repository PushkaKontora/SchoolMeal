from datetime import date

from pydantic import BaseModel

from app.nutrition.api.dto import MealtimeDTO


class ResumePupilOnDayBody(BaseModel):
    day: date


class CancelPupilForPeriodBody(BaseModel):
    start: date
    end: date
    reason: str | None


class UpdateMealtimesBody(BaseModel):
    mealtimes: dict[MealtimeDTO, bool]
