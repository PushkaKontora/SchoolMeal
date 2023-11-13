from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.children.domain.meal_plan import MealPlan
from app.children.domain.school_class import SchoolClass


@dataclass(eq=True, frozen=True)
class ChildID:
    value: str


@dataclass(eq=True, frozen=True)
class LastName:
    value: str


@dataclass(eq=True, frozen=True)
class FirstName:
    value: str


class Child(BaseModel):
    id: ChildID
    last_name: LastName
    first_name: FirstName
    school_class: SchoolClass
    meal_plan: MealPlan
