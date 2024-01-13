from uuid import uuid4

import pytest

from app.nutrition.domain.parent import Parent
from app.nutrition.domain.periods import CancellationPeriodSequence
from app.nutrition.domain.pupil import MealPlan, Name, Pupil, PupilID


@pytest.fixture
def pupil() -> Pupil:
    return Pupil(
        id=PupilID(),
        last_name=Name("Иванов"),
        first_name=Name("Иван"),
        patronymic=Name("Иванович"),
        meal_plan=MealPlan(breakfast=True, dinner=True, snacks=True),
        preferential_certificate=None,
        cancellation_periods=CancellationPeriodSequence(periods=tuple()),
    )


@pytest.fixture
def parent() -> Parent:
    return Parent(
        id=uuid4(),
        child_ids=set(),
    )
