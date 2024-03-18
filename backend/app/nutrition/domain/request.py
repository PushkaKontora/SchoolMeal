from dataclasses import dataclass
from datetime import date, datetime
from enum import IntEnum, unique

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import NutritionStatus, Pupil, PupilID
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.time import get_submitting_deadline_within_day, has_submitting_deadline_come


class CannotSubmitAfterDeadline:
    def __init__(self, deadline: datetime) -> None:
        self.deadline = deadline


@unique
class RequestStatus(IntEnum):
    PREFILLED = 0
    SUBMITTED = 1


@dataclass
class Declaration:
    pupil_id: PupilID
    mealtimes: set[Mealtime]
    nutrition: NutritionStatus

    def __hash__(self) -> int:
        return hash(self.pupil_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Declaration) and self.pupil_id == other.pupil_id

    @classmethod
    def declare(cls, pupil: Pupil) -> "Declaration":
        return cls(pupil_id=pupil.id, mealtimes=pupil.mealtimes, nutrition=pupil.nutrition)


@dataclass
class Request:
    class_id: ClassID
    on_date: date
    mealtimes: set[Mealtime]
    declarations: set[Declaration]
    status: RequestStatus

    @property
    def can_be_resubmitted_yet(self) -> bool:
        return not has_submitting_deadline_come(self.on_date)

    def submit_manually(self) -> Result["Request", CannotSubmitAfterDeadline]:
        if has_submitting_deadline_come(self.on_date):
            return Err(CannotSubmitAfterDeadline(deadline=get_submitting_deadline_within_day(self.on_date)))

        self.status = RequestStatus.SUBMITTED

        return Ok(self)
