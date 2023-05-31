from datetime import datetime

from pydantic import validator

from app.utils.entity import Entity


class DeclaredPupilSchema(Entity):
    id: str
    breakfast: bool
    lunch: bool
    dinner: bool
    preferential: bool


class MealRequestIn(Entity):
    meal_id: int
    pupils: list[DeclaredPupilSchema]

    @validator("pupils")
    def pupil_ids_should_be_unique(cls, value: list[DeclaredPupilSchema]) -> list[DeclaredPupilSchema]:
        actual = [pupil.id for pupil in value]
        expected = set(actual)

        if len(actual) != len(expected):
            raise ValueError("Pupil ids should be unique")

        return value


class MealRequestOut(Entity):
    id: int
    creator_id: int
    meal_id: int
    created_at: datetime
