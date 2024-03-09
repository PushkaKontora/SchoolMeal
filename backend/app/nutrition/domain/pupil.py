from dataclasses import dataclass
from datetime import date, datetime

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.time import (
    Day,
    Period,
    Timeline,
    get_submitting_deadline_within_day,
    has_submitting_deadline_come,
)
from app.shared.domain.pupil import PupilID
from app.shared.domain.school_class import ClassID


class CannotResumeAfterDeadline:
    def __init__(self, deadline: datetime) -> None:
        self.deadline = deadline


class CannotCancelAfterDeadline:
    def __init__(self, deadline: datetime) -> None:
        self.deadline = deadline


@dataclass
class Pupil:
    id: PupilID
    class_id: ClassID
    mealtimes: set[Mealtime]
    preferential_until: date | None
    cancelled_periods: Timeline

    def does_eat(self, day: Day, mealtime: Mealtime) -> bool:
        return mealtime in self.mealtimes and day not in self.cancelled_periods

    def resume_on_day(self, day: Day) -> Result["Pupil", CannotResumeAfterDeadline]:
        if has_submitting_deadline_come(day.value):
            return Err(CannotResumeAfterDeadline(deadline=get_submitting_deadline_within_day(day.value)))

        self.cancelled_periods.exclude(day)

        return Ok(self)

    def cancel_for_period(self, period: Period) -> Result["Pupil", CannotCancelAfterDeadline]:
        for day in period:
            if not has_submitting_deadline_come(day):
                continue

            return Err(CannotCancelAfterDeadline(deadline=get_submitting_deadline_within_day(day)))

        self.cancelled_periods.insert(period)

        return Ok(self)

    def resume_on_mealtime(self, mealtime: Mealtime) -> Ok["Pupil"]:
        self.mealtimes.add(mealtime)

        return Ok(self)

    def cancel_from_mealtime(self, mealtime: Mealtime) -> Ok["Pupil"]:
        if mealtime in self.mealtimes:
            self.mealtimes.remove(mealtime)

        return Ok(self)
