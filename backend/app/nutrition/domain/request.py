from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Iterable

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.domain.times import Day, combine, now


class CannotSentRequestAfterDeadline:
    def __init__(self, deadline: time) -> None:
        self.deadline = deadline


@dataclass
class Request:
    class_id: ClassID
    on_date: date
    mealtimes: dict[Mealtime, set[PupilID]]
    created_at: datetime

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Request) and (self.class_id, self.on_date) == (other.class_id, other.on_date)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @classmethod
    def submit_to_canteen(
        cls, school_class: SchoolClass, pupils: Iterable[Pupil], overrides: dict[PupilID, set[Mealtime]], on_date: date
    ) -> Result["Request", CannotSentRequestAfterDeadline]:
        deadline = combine(on_date, time(hour=22))

        if now() >= deadline:
            return Err(CannotSentRequestAfterDeadline(deadline=deadline.timetz()))

        mealtimes: dict[Mealtime, set[PupilID]] = {mealtime_: set() for mealtime_ in school_class.mealtimes}

        for pupil in pupils:
            for mealtime, request in mealtimes.items():
                eats = pupil.does_eat(day=Day(on_date), mealtime=mealtime)

                if pupil.id in overrides:
                    eats = mealtime in overrides[pupil.id]

                if eats:
                    request.add(pupil.id)

        return Ok(
            cls(
                class_id=school_class.id,
                on_date=on_date,
                mealtimes=mealtimes,
                created_at=now(),
            )
        )
