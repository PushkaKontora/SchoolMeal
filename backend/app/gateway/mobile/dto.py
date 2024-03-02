from datetime import date

from pydantic import BaseModel


class ResumePupilOnDayIn(BaseModel):
    day: date


class CancelPupilForPeriodIn(BaseModel):
    start: date
    end: date


class UpdateMealtimesIn(BaseModel):
    breakfast: bool | None = None
    dinner: bool | None = None
    snacks: bool | None = None


class FeedbackTextIn(BaseModel):
    text: str
