import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.school_class import SchoolClass
from app.nutrition.domain.time import Timeline
from app.shared.domain.pupil import PupilID
from app.shared.domain.school_class import ClassID


@pytest.fixture
def school_class() -> SchoolClass:
    return SchoolClass(id=ClassID.generate(), mealtimes={Mealtime.DINNER})


@pytest.fixture
def pupil(school_class: SchoolClass) -> Pupil:
    return Pupil(
        id=PupilID.generate(),
        class_id=school_class.id,
        mealtimes={Mealtime.DINNER},
        preferential_until=None,
        cancelled_periods=Timeline(),
    )
