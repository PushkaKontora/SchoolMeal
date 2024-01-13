from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum, unique
from uuid import UUID

from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan, PupilID
from app.nutrition.domain.school_class import SchoolClass


class RequestIsAlreadySubmitted(Exception):
    pass


class CannotOverrideRequestAfter(Exception):
    def __init__(self, time: datetime) -> None:
        self.time = time


class RequestIsAlreadyToBeSubmitted(Exception):
    def __init__(self, status: "Status") -> None:
        self.status = status


@unique
class Status(IntEnum):
    PREFILLED = 0
    FROZEN = 10
    SUBMITTED = 20


@dataclass
class Request:
    class_id: UUID
    on_date: Day
    pupils: dict[PupilID, MealPlan]
    status: Status

    def prepare(self, pupils: dict[PupilID, MealPlan]) -> None:
        """
        :raise RequestIsAlreadyToBeSubmitted: заявка уже готова к отправке и не может быть изменена
        """

        if self.status is not Status.PREFILLED:
            raise RequestIsAlreadyToBeSubmitted(self.status)

        for pupil_id, new_meal_plan in pupils.items():
            if pupil_id not in self.pupils:
                continue

            self.pupils[pupil_id] = new_meal_plan

    def freeze(self) -> None:
        """
        :raise RequestIsAlreadySubmitted: заявка уже отправлена
        """

        if self.status is Status.SUBMITTED:
            raise RequestIsAlreadySubmitted

        self.status = Status.FROZEN

    def submit(self) -> None:
        """
        :raise RequestIsAlreadySubmitted: заявка уже отправлена
        """

        if self.status is Status.SUBMITTED:
            raise RequestIsAlreadySubmitted

        self.status = Status.SUBMITTED

    @classmethod
    def prefill(cls, school_class: SchoolClass, on_date: Day) -> "Request":
        return cls(
            class_id=school_class.id,
            on_date=on_date,
            pupils={pupil.id: pupil.meal_plan for pupil in school_class.pupils},
            status=Status.PREFILLED,
        )
