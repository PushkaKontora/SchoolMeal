from datetime import date

from pydantic import BaseModel

from app.nutrition.api.dto import ResumedPupilIn


class SubmitRequestBody(BaseModel):
    on_date: date
    overrides: set[ResumedPupilIn]
