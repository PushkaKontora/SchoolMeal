import secrets

import pytest

from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriodSequence
from app.nutrition.domain.pupil import FirstName, LastName, Pupil, PupilID


@pytest.fixture
def pupil(meal_plan: MealPlan) -> Pupil:
    return Pupil(
        id=PupilID(secrets.token_hex(10)),
        last_name=LastName("Иванов"),
        first_name=FirstName("Иван"),
        meal_plan=meal_plan,
        preferential_certificate=None,
        cancellation_periods=CancellationPeriodSequence(periods=tuple()),
    )


@pytest.fixture
def meal_plan() -> MealPlan:
    return MealPlan(has_breakfast=True, has_dinner=True, has_snacks=True)


@pytest.fixture
def new_plan(meal_plan: MealPlan) -> MealPlan:
    return MealPlan(
        has_breakfast=not meal_plan.has_breakfast,
        has_dinner=not meal_plan.has_dinner,
        has_snacks=not meal_plan.has_snacks,
    )
