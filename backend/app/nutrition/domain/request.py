from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Iterable
from uuid import UUID, uuid4

from result import Err, Ok, Result

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.nutrition.domain.times import Day, combine, now


class AlreadyBeenPreparedForSending:
    pass


@dataclass(frozen=True)
class RequestID:
    value: UUID

    @classmethod
    def generate(cls) -> "RequestID":
        return cls(uuid4())


@dataclass
class Request:
    id: RequestID
    class_id: ClassID
    on_date: date
    mealtimes: dict[Mealtime, set[PupilID]]
    created_at: datetime

    def edit(self, pupils: Iterable[Pupil]) -> Result["Request", AlreadyBeenPreparedForSending]:
        if now() >= combine(self.on_date, time(hour=22)):
            return Err(AlreadyBeenPreparedForSending())

        for mealtime, request in self.mealtimes.items():
            for pupil in pupils:
                if pupil.does_eat(day=Day(self.on_date), mealtime=mealtime):
                    request.add(pupil.id)
                    continue

                if pupil.id in request:
                    request.remove(pupil.id)

        return Ok(self)

    @classmethod
    def submit_to_canteen(cls, school_class: SchoolClass, pupils: Iterable[Pupil], on_date: date) -> "Request":
        mealtimes: dict[Mealtime, set[PupilID]] = {mealtime: set() for mealtime in school_class.mealtimes}

        day = Day(on_date)

        for pupil in pupils:
            for mealtime_, request in mealtimes.items():
                if not pupil.does_eat(day, mealtime_):
                    continue

                request.add(pupil.id)

        return cls(
            id=RequestID.generate(),
            class_id=school_class.id,
            on_date=on_date,
            mealtimes=mealtimes,
            created_at=now(),
        )
