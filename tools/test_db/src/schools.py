import secrets
import time
from enum import Enum
from itertools import cycle
from uuid import uuid4

import names
from pydantic import BaseModel


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


class MealPlan(BaseModel):
    status: MealStatus


class Pupil(BaseModel):
    id: str
    last_name: str
    first_name: str
    meal_plan: MealPlan


class SchoolClass(BaseModel):
    id: str
    number: int
    literal: str
    pupils: list["Pupil"]


class School(BaseModel):
    id: str
    name: str
    school_classes: list[SchoolClass]


def generate_schools(amount: int = 3) -> list[School]:
    return [
        School(
            id=str(uuid4()),
            name=f"school #{time.time()}",
            school_classes=_generate_school_classes(),
        )
        for i in range(amount)
    ]


def _generate_school_classes() -> list[SchoolClass]:
    return [SchoolClass(id=str(uuid4()), number=i, literal="A", pupils=_generate_pupils()) for i in range(1, 12)]


def _generate_pupils(amount: int = 30) -> list[Pupil]:
    statuses = cycle(MealStatus)

    return [
        Pupil(
            id=secrets.token_hex(10),
            last_name=names.get_last_name(),
            first_name=names.get_first_name(),
            meal_plan=MealPlan(status=next(statuses)),
        )
        for _ in range(amount)
    ]
