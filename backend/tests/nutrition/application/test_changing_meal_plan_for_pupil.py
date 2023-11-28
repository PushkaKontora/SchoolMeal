import pytest

from app.nutrition.application.repositories import NotFoundPupil
from app.nutrition.application.services import NutritionService
from app.nutrition.domain.meal_plan import MealPlan


async def test_change_meal_plan_for_non_existing_pupil(new_plan: MealPlan, nutrition_service: NutritionService):
    with pytest.raises(NotFoundPupil):
        await nutrition_service.change_meal_plan_for_pupil(
            pupil_id="1337",
            has_breakfast=new_plan.has_breakfast,
            has_dinner=new_plan.has_dinner,
            has_snacks=new_plan.has_snacks,
        )
