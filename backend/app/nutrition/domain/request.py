from dataclasses import dataclass
from datetime import date, time
from enum import IntEnum, unique

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import PupilID
from app.nutrition.domain.time import get_submitting_deadline_within_day, has_submitting_deadline_come
from app.shared.domain.school_class import ClassID


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

    def submit_manually(self) -> Result["Request", CannotSubmitAfterDeadline]:
        if has_submitting_deadline_come(self.on_date):
            return Err(CannotSubmitAfterDeadline(deadline=get_submitting_deadline_within_day(self.on_date).timetz()))

        self.status = Status.SUBMITTED

        return Ok(self)
