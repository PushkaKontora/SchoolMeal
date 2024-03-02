from datetime import date

from pydantic import BaseModel

from app.nutrition.domain.mealtime import Mealtime


class OverriddenPupilIn(BaseModel):
    pupil_id: str
    mealtimes: set[Mealtime]


class SubmitRequestIn(BaseModel):
    on_date: date
    overrides: list[OverriddenPupilIn]
