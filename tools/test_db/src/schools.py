import itertools
import secrets
import time
from datetime import date, datetime, timedelta, timezone
from enum import Enum
from uuid import uuid4

import names
from pydantic import BaseModel


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


class MealPlan(BaseModel):
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class PreferentialCertificate(BaseModel):
    ends_at: date


class Pupil(BaseModel):
    id: str
    last_name: str
    first_name: str
    meal_plan: MealPlan
    preferential_certificate: PreferentialCertificate | None
    meal_status: MealStatus


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
        for _ in range(amount)
    ]


def _generate_school_classes() -> list[SchoolClass]:
    return [SchoolClass(id=str(uuid4()), number=i, literal="A", pupils=_generate_pupils()) for i in range(1, 12)]


def _generate_pupils(amount: int = 30) -> list[Pupil]:
    statuses = itertools.cycle(MealStatus)
    meal_plans = itertools.cycle(
        MealPlan(has_breakfast=b, has_dinner=d, has_snacks=s) for b, d, s in itertools.product([False, True], repeat=3)
    )

    now = datetime.now(timezone.utc).now()
    past, future = now - timedelta(days=30), now + timedelta(days=30)
    certificates = itertools.cycle(
        [PreferentialCertificate(ends_at=past), PreferentialCertificate(ends_at=future), None]
    )

    return [
        Pupil(
            id=secrets.token_hex(10),
            last_name=names.get_last_name(),
            first_name=names.get_first_name(),
            meal_plan=next(meal_plans),
            meal_status=next(statuses),
            preferential_certificate=next(certificates),
        )
        for _ in range(amount)
    ]
