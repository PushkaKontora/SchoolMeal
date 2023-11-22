from datetime import date

from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriod, SpecifiedReason
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


async def cancel_pupil_nutrition_for_period(
    pupil_id: str, starts_at: date, ends_at: date, reason: str | None, pupils_repository: IPupilsRepository
) -> list[CancellationPeriod]:
    """
    :raise NotFoundPupil: не найден ученик
    :raise SpecifiedReasonCannotBeEmpty: текст причины не может быть пустым
    :raise ExceededMaxLengthReason: превышена максимальная длина текста причины
    :raise EndCannotBeGreaterThanStart: дата начала периода больше, чем конечная дата
    """

    pupil = await pupils_repository.get_by_id(pupil_id=PupilID(pupil_id))

    reasons = {SpecifiedReason(reason)} if reason is not None else {}
    period = CancellationPeriod(starts_at=starts_at, ends_at=ends_at, reasons=frozenset(reasons))

    pupil.cancel_nutrition(period=period)
    await pupils_repository.update(pupil)

    return list(pupil.cancellation_periods)
