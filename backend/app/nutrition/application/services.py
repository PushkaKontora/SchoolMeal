from datetime import date

from app.nutrition.application.repositories import IPupilsRepository
from app.nutrition.domain.meal_plan import MealPlan
from app.nutrition.domain.periods import CancellationPeriod, Day, SpecifiedReason
from app.nutrition.domain.pupil import Pupil, PupilID
from app.shared.unit_of_work import UnitOfWork


class NutritionService:
    def __init__(self, unit_of_work: UnitOfWork, pupils_repository: IPupilsRepository) -> None:
        self._unit_of_work = unit_of_work
        self._pupils = pupils_repository

    async def get_pupil(self, pupil_id: str) -> Pupil:
        """
        :raise NotFoundPupil: не найден ученик
        """
        return await self._pupils.get_by_id(pupil_id=PupilID(pupil_id))

    async def change_meal_plan_for_pupil(
        self, pupil_id: str, has_breakfast: bool, has_dinner: bool, has_snacks: bool
    ) -> None:
        """
        :raise NotFoundPupil: не найден ученик
        """

        async with self._unit_of_work as session:
            pupil = await self._pupils.get_by_id(pupil_id=PupilID(pupil_id))

            plan = MealPlan(has_breakfast=has_breakfast, has_dinner=has_dinner, has_snacks=has_snacks)
            pupil.update_meal_plan(plan)
            await self._pupils.update(pupil)

            await session.commit()

    async def cancel_pupil_nutrition_for_period(
        self, pupil_id: str, starts_at: date, ends_at: date, reason: str | None
    ) -> list[CancellationPeriod]:
        """
        :raise NotFoundPupil: не найден ученик
        :raise SpecifiedReasonCannotBeEmpty: текст причины не может быть пустым
        :raise ExceededMaxLengthReason: превышена максимальная длина текста причины
        :raise EndCannotBeGreaterThanStart: дата начала периода больше, чем конечная дата
        """

        async with self._unit_of_work as session:
            pupil = await self._pupils.get_by_id(pupil_id=PupilID(pupil_id))

            reasons = {SpecifiedReason(reason)} if reason is not None else {}
            period = CancellationPeriod(starts_at=starts_at, ends_at=ends_at, reasons=frozenset(reasons))

            updated_periods = pupil.cancel_nutrition(period=period)
            await self._pupils.update(pupil)

            await session.commit()

        return list(updated_periods)

    async def resume_pupil_nutrition_on_day(self, pupil_id: str, date_: date) -> list[CancellationPeriod]:
        """
        :raise NotFoundPupil: не найден ученик
        """

        async with self._unit_of_work as session:
            pupil = await self._pupils.get_by_id(pupil_id=PupilID(pupil_id))

            updated_periods = pupil.resume_nutrition(day=Day(date_))
            await self._pupils.update(pupil)

            await session.commit()

        return list(updated_periods)
