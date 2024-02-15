from datetime import date

from pydantic import BaseModel

from app.nutrition.domain.mealtime import Mealtime


class OverridenPupilIn(BaseModel):
    pupil_id: str
    mealtimes: set[Mealtime]


class SubmitRequestIn(BaseModel):
    on_date: date
    overrides: list[OverridenPupilIn]
