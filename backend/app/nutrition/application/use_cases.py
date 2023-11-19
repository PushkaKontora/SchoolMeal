from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.pupil import Pupil, PupilID


async def get_pupil(pupil_id: str, pupils_repository: IPupilsRepository) -> Pupil:
    """
    :raise NotFoundPupil:
    """
    return await pupils_repository.get_by_id(pupil_id=PupilID(pupil_id))


async def make_meal_plan_for_pupil(
    pupil_id: str, has_breakfast: bool, has_dinner: bool, has_snacks: bool, pupils_repository: IPupilsRepository
) -> None:
    """
    :raise NotFoundPupil:
    """
    pupil = await pupils_repository.get_by_id(pupil_id=PupilID(pupil_id))

    plan = MealPlan(has_breakfast=has_breakfast, has_dinner=has_dinner, has_snacks=has_snacks)
    pupil.update_meal_plan(plan)
    await pupils_repository.update(pupil)
