from datetime import date

from app.nutrition.commands.context import NutritionContext
from app.nutrition.domain.periods import Day
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class ResumeNutritionCommand(Command):
    pupil_id: str
    day: date


class ResumeNutritionCommandHandler(ICommandHandler[ResumeNutritionCommand]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: ResumeNutritionCommand) -> None:
        """
        :raise NotFoundPupil: не найден ученик
        """

        async with self._unit_of_work as context:
            pupil = await context.pupils.get_by_id(pupil_id=command.pupil_id)

            pupil.resume_nutrition(day=Day(command.day))
            await context.pupils.update(pupil)

            await self._unit_of_work.commit()
