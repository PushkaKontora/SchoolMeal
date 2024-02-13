from datetime import date

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.dto import CancellationPeriodOut
from app.nutrition.domain.times import Day
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class ResumeNutritionCommand(Command):
    pupil_id: str
    day: date


class ResumeNutritionCommandHandler(ICommandHandler[ResumeNutritionCommand, list[CancellationPeriodOut]]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: ResumeNutritionCommand) -> list[CancellationPeriodOut]:
        """
        :raise NotFoundPupil: не найден ученик
        :raise CannotResumeNutritionAfterTime: нельзя ставить на питание после 10 утра по ЕКБ
        """

        async with self._unit_of_work as context:
            pupil = await context.pupils.get_by_id(pupil_id=command.pupil_id)

            pupil.resume_nutrition_on_day(day=Day(command.day))
            await context.pupils.update(pupil)

            await self._unit_of_work.commit()

        return list(map(CancellationPeriodOut.from_model, pupil.cancellation))
