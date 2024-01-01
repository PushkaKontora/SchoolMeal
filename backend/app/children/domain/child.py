from pydantic.dataclasses import dataclass

from app.children.domain.meal_plan import MealPlan
from app.children.domain.school_class import SchoolClass
from app.shared.domain import Entity, ValueObject


@dataclass(eq=True, frozen=True)
class ChildID(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class LastName(ValueObject):
    value: str


@dataclass(eq=True, frozen=True)
class FirstName(ValueObject):
    value: str


@dataclass
class Child(Entity):
    id: ChildID
    last_name: LastName
    first_name: FirstName
    school_class: SchoolClass
    meal_plan: MealPlan
