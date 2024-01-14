from dataclasses import dataclass
from datetime import datetime, time
from uuid import UUID

from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan, PupilID
from app.nutrition.domain.school_class import SchoolClass
from app.shared.domain import timezones


class RequestCannotBeEditedAfter(Exception):
    pass


@dataclass
class PupilInfo:
    id: PupilID
    plan: MealPlan
    preferential: bool


@dataclass
class DraftRequest:
    class_id: UUID
    on_date: Day
    pupils: dict[PupilID, MealPlan]

    def edit(self, pupils: dict[PupilID, MealPlan]) -> None:
        """
        :raise RequestCannotBeUpdatedAfter: заявка не может быть отредактирована
        """

        if datetime.now(timezones.yekaterinburg) > self.on_date.combine(time(hour=10, tzinfo=timezones.yekaterinburg)):
            raise RequestCannotBeEditedAfter

        self.pupils.update(pupils)

    @classmethod
    def prefill(cls, school_class: SchoolClass, on_date: Day) -> "DraftRequest":
        return cls(
            class_id=school_class.id,
            on_date=on_date,
            pupils={pupil.id: pupil.meal_plan for pupil in school_class.pupils},
        )


@dataclass
class Request:
    class_id: UUID
    on_date: Day
    pupils: list[PupilInfo]
