from enum import Enum

from app.children.domain.child import Child
from app.children.domain.meal_plan import MealPlan, MealStatus
from app.children.domain.school import School
from app.children.domain.school_class import SchoolClass
from app.common.api.schemas import FrontendModel


class SchoolOut(FrontendModel):
    id: str
    name: str

    @classmethod
    def from_model(cls, school: School) -> "SchoolOut":
        return cls(
            id=str(school.id),
            name=school.name.value,
        )


class SchoolClassOut(FrontendModel):
    id: str
    school: SchoolOut
    number: int
    literal: str

    @classmethod
    def from_model(cls, school_class: SchoolClass) -> "SchoolClassOut":
        return cls(
            id=str(school_class.id),
            school=SchoolOut.from_model(school_class.school),
            number=school_class.number.value,
            literal=school_class.literal.value,
        )


class MealStatusOut(str, Enum):
    PREFERENTIAL = "Питается льготно"
    PAID = "Питается платно"
    NONE = "Не питается"

    @classmethod
    def from_model(cls, status: MealStatus) -> "MealStatusOut":
        mapper = {
            MealStatus.PREFERENTIAL: cls.PREFERENTIAL,
            MealStatus.PAID: cls.PAID,
            MealStatus.NONE: cls.NONE,
        }
        return mapper[status]


class MealPlanOut(FrontendModel):
    status: MealStatusOut

    @classmethod
    def from_model(cls, meal_plan: MealPlan) -> "MealPlanOut":
        return cls(status=MealStatusOut.from_model(meal_plan.status))


class ChildOut(FrontendModel):
    id: str
    last_name: str
    first_name: str
    school_class: SchoolClassOut
    meal_plan: MealPlanOut

    @classmethod
    def from_model(cls, child: Child) -> "ChildOut":
        return cls(
            id=child.id.value,
            last_name=child.last_name.value,
            first_name=child.first_name.value,
            school_class=SchoolClassOut.from_model(child.school_class),
            meal_plan=MealPlanOut.from_model(child.meal_plan),
        )
