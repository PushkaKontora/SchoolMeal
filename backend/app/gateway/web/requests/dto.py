from datetime import date

from pydantic import BaseModel

from app.nutrition.api.dto import ResumedPupilIn
from app.structure.api.dto import SchoolClassType


class SubmitRequestBody(BaseModel):
    on_date: date
    overrides: set[ResumedPupilIn]


class GetOrPrefillRequestParams(BaseModel):
    on_date: date


class GetPortionReportBySubmittedRequestsParams(BaseModel):
    class_type: SchoolClassType
    on_date: date
