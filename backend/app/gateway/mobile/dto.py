from datetime import date

from pydantic import BaseModel

from app.nutrition.domain.mealtime import Mealtime


class MealtimeTogglerIn(BaseModel):
    mealtime: Mealtime
    enabled: bool


class ResumeOnDayIn(BaseModel):
    day: date


class CancelForPeriodIn(BaseModel):
    start: date
    end: date
