from datetime import datetime

from pydantic import validator

from app.utils.entity import Entity


class DeclaredPupilIn(Entity):
    id: str
    breakfast: bool
    lunch: bool
    dinner: bool
    preferential: bool


class DeclaredPupilListIn(Entity):
    pupils: list[DeclaredPupilIn]

    @validator("pupils")
    def pupil_ids_should_be_unique(cls, value: list[DeclaredPupilIn]) -> list[DeclaredPupilIn]:
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
