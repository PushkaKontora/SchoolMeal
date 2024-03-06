from dataclasses import dataclass
from datetime import date, datetime, time
from enum import IntEnum, unique

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import combine, now, yekaterinburg


class CannotSubmitAfterDeadline:
    def __init__(self, deadline: time) -> None:
        self.deadline = deadline


@unique
class Status(IntEnum):
    PREFILLED = 0
    SUBMITTED = 1


@dataclass
class Request:
    class_id: ClassID
    on_date: date
    mealtimes: dict[Mealtime, set[PupilID]]
    status: Status

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Request) and (self.class_id, self.on_date) == (other.class_id, other.on_date)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def deadline(self) -> datetime:
        return combine(self.on_date, time(hour=22, tzinfo=yekaterinburg))

    def submit_manually(self) -> Result["Request", CannotSubmitAfterDeadline]:
        if now() >= self.deadline:
            return Err(CannotSubmitAfterDeadline(deadline=self.deadline.timetz()))

        self.status = Status.SUBMITTED

        return Ok(self)
