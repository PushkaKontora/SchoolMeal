import pytest

from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.application.services import NutritionService
from app.nutrition.domain.pupil import Pupil
from tests.nutrition.application.repositories import LocalPupilsRepository


@pytest.fixture
def pupils_repository(pupil: Pupil) -> IPupilsRepository:
    return LocalPupilsRepository(pupils=[pupil])


@pytest.fixture
def nutrition_service(pupils_repository: IPupilsRepository) -> NutritionService:
    return NutritionService(pupils_repository=pupils_repository)
