from uuid import uuid4

import pytest

from app.children.domain.child import Child, ChildID, FirstName, LastName
from app.children.domain.meal_plan import MealPlan, MealStatus
from app.children.domain.parent import Parent
from app.children.domain.school import School, SchoolName
from app.children.domain.school_class import ClassLiteral, ClassNumber, SchoolClass


@pytest.fixture
def school() -> School:
    return School(id=uuid4(), name=SchoolName("school #1"))


@pytest.fixture
def school_class(school: School) -> SchoolClass:
    return SchoolClass(
        id=uuid4(),
        school=school,
        number=ClassNumber(1),
        literal=ClassLiteral("A"),
    )


@pytest.fixture
def meal_plan() -> MealPlan:
    return MealPlan(status=MealStatus.PAID)


@pytest.fixture
def child(school_class: SchoolClass, meal_plan: MealPlan) -> Child:
    return Child(
        id=ChildID("abc"),
        last_name=LastName("Дыков"),
        first_name=FirstName("Лима"),
        school_class=school_class,
        meal_plan=meal_plan,
    )


@pytest.fixture
def parent() -> Parent:
    return Parent(id=uuid4(), child_ids=set())
