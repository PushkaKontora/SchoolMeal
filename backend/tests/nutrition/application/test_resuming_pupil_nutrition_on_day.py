from datetime import date

import pytest

from app.nutrition.application.repositories import NotFoundPupil
from app.nutrition.application.services import NutritionService
from app.nutrition.domain.pupil import Pupil


async def test_resuming_nutrition(pupil: Pupil, nutrition_service: NutritionService):
    periods = await nutrition_service.resume_pupil_nutrition_on_day(pupil_id=pupil.id.value, date_=date(2023, 11, 10))

    assert len(periods) == 2

    left, right = periods
    assert (left.starts_at.day, left.ends_at.day) == (1, 9)
    assert (right.starts_at.day, right.ends_at.day) == (11, 15)


async def test_resuming_nutrition_at_non_existing_pupil(nutrition_service: NutritionService):
    with pytest.raises(NotFoundPupil):
        await nutrition_service.resume_pupil_nutrition_on_day(pupil_id="123", date_=date(2023, 11, 29))


@pytest.fixture(autouse=True)
async def cancel_nutrition(pupil: Pupil, nutrition_service: NutritionService) -> None:
    await nutrition_service.cancel_pupil_nutrition_for_period(
        pupil_id=pupil.id.value,
        starts_at=date(2023, 11, 1),
        ends_at=date(2023, 11, 15),
        reason="Простыл",
    )
