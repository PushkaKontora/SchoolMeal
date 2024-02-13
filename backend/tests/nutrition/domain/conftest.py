import pytest

from app.nutrition.domain.pupil import Pupil, PupilID, PupilName
from app.nutrition.domain.school_class import ClassID
from app.nutrition.domain.times import Timeline


@pytest.fixture
def pupil() -> Pupil:
    return Pupil(
        id=PupilID.generate(),
        class_id=ClassID.generate(),
        last_name=PupilName("Пупкин"),
        first_name=PupilName("Вася"),
        patronymic=None,
        mealtimes=set(),
        preferential_until=None,
        cancellation=Timeline(),
    )
