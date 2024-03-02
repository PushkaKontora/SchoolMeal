import itertools as it
import random
import secrets
from datetime import date, datetime, timedelta, timezone
from enum import IntEnum
from uuid import UUID, uuid4

from pydantic import BaseModel


class Mealtime(IntEnum):
    BREAKFAST = 0
    DINNER = 10
    SNACKS = 20


class Pupil(BaseModel):
    id: str
    last_name: str
    first_name: str
    patronymic: str | None
    preferential_until: date | None
    mealtimes: set[Mealtime]


class SchoolClass(BaseModel):
    id: str
    number: int
    literal: str
    mealtimes: set[Mealtime]
    pupils: list["Pupil"]


class Teacher(BaseModel):
    id: str
    last_name: str
    first_name: str
    patronymic: str


class Parent(BaseModel):
    id: str
    last_name: str
    first_name: str
    email: str
    phone: str


class School(BaseModel):
    id: str
    name: str
    teacher: Teacher
    school_classes: list[SchoolClass]
    parent: Parent


def generate_school() -> School:
    return School(
        id=str(uuid4()),
        name="МБОУ СОШ №1337",
        school_classes=_generate_school_classes(),
        teacher=Teacher(id=str(uuid4()), last_name="Лыкова", first_name="Агафья", patronymic="Андреевна"),
        parent=Parent(
            id=str(UUID("844c4372-52eb-4452-b314-728583ee5fbf")),
            last_name="Кузьмин",
            first_name="Кузьмич",
            email="serious_kys@gmail.com",
            phone="8005553535",
        ),
    )


def _generate_school_classes() -> list[SchoolClass]:
    mealtimes = it.cycle([*it.combinations(Mealtime, r=3), *it.combinations(Mealtime, r=2)])

    return [
        SchoolClass(id=str(uuid4()), number=i, literal="A", pupils=_generate_pupils(), mealtimes=set(next(mealtimes)))
        for i in range(1, 12)
    ]


def _generate_pupils(amount: int = 5) -> list[Pupil]:
    last_names = ("Петров", "Cидоров", "Перов", "Самков", "Лыков", "Голендухин")
    first_names = ("Василий", "Дмитрий", "Илья", "Никита", "Владимир", "Пётр")
    patronymics = ("Евгеньевич", "Юрьевич", "Дмитриевич", "Владимирович", None)

    mealtimes = it.cycle([*it.combinations(Mealtime, r=1), *it.combinations(Mealtime, r=2)])

    now = datetime.now(timezone.utc).now()
    preferential_until_dates = it.cycle([now - timedelta(days=30), now + timedelta(days=30), None])

    return [
        Pupil(
            id=secrets.token_hex(10),
            last_name=random.choice(last_names),
            first_name=random.choice(first_names),
            patronymic=random.choice(patronymics),
            mealtimes=set(next(mealtimes)),
            preferential_until=next(preferential_until_dates),
        )
        for _ in range(amount)
    ]
