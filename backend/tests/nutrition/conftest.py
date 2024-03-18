import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.time import Timeline
from app.shared.domain.personal_info import FullName


@pytest.fixture
def school_class() -> SchoolClass:
    return SchoolClass(
        id=ClassID.generate(), teacher_id=None, number=Number(1), literal=Literal("И"), mealtimes={Mealtime.DINNER}
    )


@pytest.fixture
def pupil(school_class: SchoolClass) -> Pupil:
    return Pupil(
        id=PupilID.generate(),
        class_id=school_class.id,
        parent_ids=set(),
        name=FullName.create("Лыков", "Дмитрий"),
        mealtimes={Mealtime.DINNER},
        preferential_until=None,
        cancelled_periods=Timeline(),
    )
