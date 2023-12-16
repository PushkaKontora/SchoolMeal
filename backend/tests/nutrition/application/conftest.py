import pytest

from app.nutrition.application.services import NutritionService
from app.nutrition.application.unit_of_work import NutritionContext
from app.nutrition.domain.pupil import Pupil
from tests.nutrition.application.repositories import LocalPupilsRepository
from tests.unit_of_work import LocalUnitOfWork


@pytest.fixture
def nutrition_service(pupil: Pupil) -> NutritionService:
    return NutritionService(
        unit_of_work=LocalUnitOfWork(
            lambda: NutritionContext(
                pupils=LocalPupilsRepository([pupil]),
            )
        )
    )
