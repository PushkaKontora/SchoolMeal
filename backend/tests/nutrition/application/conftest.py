import pytest

from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.domain.pupil import Pupil
from tests.nutrition.application.repositories import LocalPupilsRepository


@pytest.fixture
def pupils_repository(pupil: Pupil) -> IPupilsRepository:
    return LocalPupilsRepository(pupils=[pupil])
