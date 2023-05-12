from datetime import date

from pydantic import Field, validator

from app.entity import Entity


class PeriodIn(Entity):
    pupil_id: str
    start_date: date
    end_date: date | None
    comment: str | None = Field(max_length=512)

    @validator("end_date")
    def validate_end_date_should_be_greater_than_start_date(cls, value: date, values: dict, **kwargs):
        start_date: date = values["start_date"]

        if value is not None and value <= start_date:
            raise ValueError("start_date should be greater than start_date")

        return value


class PeriodOut(PeriodIn):
    pass
