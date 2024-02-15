import secrets
from dataclasses import dataclass
from datetime import date

from result import Ok

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Day, Period, Timeline


@dataclass(frozen=True)
class PupilID:
    value: str

    @classmethod
    def generate(cls) -> "PupilID":
        return cls(secrets.token_hex(10))


@dataclass
class Pupil:
    id: PupilID
    class_id: ClassID
    mealtimes: set[Mealtime]
    preferential_until: date | None
    cancellation: Timeline

    def does_eat(self, day: Day, mealtime: Mealtime) -> bool:
        return mealtime in self.mealtimes and day not in self.cancellation

    def resume_on_day(self, day: Day) -> Ok["Pupil"]:
        self.cancellation.exclude(day)

        return Ok(self)

    def cancel_for_period(self, period: Period) -> Ok["Pupil"]:
        self.cancellation.insert(period)

        return Ok(self)

    def resume_on_mealtime(self, mealtime: Mealtime) -> Ok["Pupil"]:
        self.mealtimes.add(mealtime)

        return Ok(self)

    def cancel_from_mealtime(self, mealtime: Mealtime) -> Ok["Pupil"]:
        if mealtime in self.mealtimes:
            self.mealtimes.remove(mealtime)

        return Ok(self)
