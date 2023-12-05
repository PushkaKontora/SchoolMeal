from unittest.mock import AsyncMock

import pytest

from app.nutrition.application.services import NutritionService
from app.nutrition.domain.pupil import Pupil
from tests.nutrition.application.repositories import LocalPupilsRepository


@pytest.fixture
def nutrition_service(pupil: Pupil) -> NutritionService:
    return NutritionService(unit_of_work=AsyncMock(), pupils_repository=LocalPupilsRepository(pupils=[pupil]))
