import pytest

from app.nutrition.application.repositories import IPupilsRepository, NotFoundPupil
from app.nutrition.application.use_cases import make_meal_plan_for_pupil
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.pupil import Pupil


async def test_making_new_plan(pupil: Pupil, new_plan: MealPlan, pupils_repository: IPupilsRepository):
    await make_meal_plan_for_pupil(
        pupil_id=pupil.id.value,
        has_breakfast=new_plan.has_breakfast,
        has_dinner=new_plan.has_dinner,
        has_snacks=new_plan.has_snacks,
        pupils_repository=pupils_repository,
    )

    pupil = await pupils_repository.get_by_id(pupil_id=pupil.id)
    assert pupil.meal_plan == new_plan


async def test_not_found_pupil(new_plan: MealPlan, pupils_repository: IPupilsRepository):
    with pytest.raises(NotFoundPupil):
        await make_meal_plan_for_pupil(
            pupil_id="abc",
            has_breakfast=new_plan.has_breakfast,
            has_dinner=new_plan.has_dinner,
            has_snacks=new_plan.has_snacks,
            pupils_repository=pupils_repository,
        )
