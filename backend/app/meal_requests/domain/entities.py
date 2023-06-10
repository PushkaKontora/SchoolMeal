from datetime import date as date_type, datetime

from pydantic import validator

from app.school_classes.domain.entities import ClassOut
from app.utils.entity import Entity


class MealRequestsGetOptions(Entity):
    school_id: int | None = None
    date: date_type | None = None


class DeclaredPupilSchema(Entity):
    id: str
    breakfast: bool
    lunch: bool
    dinner: bool
    preferential: bool


class DeclaredPupilListIn(Entity):
    pupils: list[DeclaredPupilSchema]

    @validator("pupils")
    def pupil_ids_should_be_unique(cls, value: list[DeclaredPupilSchema]) -> list[DeclaredPupilSchema]:
        actual = [pupil.id for pupil in value]
        expected = set(actual)

        if len(actual) != len(expected):
            raise ValueError("Pupil ids should be unique")

        return value


class MealRequestPutIn(DeclaredPupilListIn):
    pass


class MealRequestIn(DeclaredPupilListIn):
    meal_id: int


class MealRequestOut(Entity):
    id: int
    creator_id: int
    meal_id: int
    created_at: datetime


class ExtendedMealRequestOut(MealRequestOut):
    date: date_type
    school_class: ClassOut
    pupils: list[DeclaredPupilSchema]
