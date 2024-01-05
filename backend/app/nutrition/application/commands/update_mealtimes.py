from app.nutrition.application.commands.context import NutritionContext
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class UpdateMealtimesCommand(Command):
    pupil_id: str
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class UpdateMealtimesCommandHandler(ICommandHandler[UpdateMealtimesCommand, None]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: UpdateMealtimesCommand) -> None:
        """
        :raise NotFoundPlan: не найден план
        """

        async with self._unit_of_work as context:
            pupil = await context.pupils.get_by_id(pupil_id=command.pupil_id)

            pupil.update_mealtimes(
                has_breakfast=command.has_breakfast,
                has_dinner=command.has_dinner,
                has_snacks=command.has_snacks,
            )
            await context.pupils.update(pupil)

            await self._unit_of_work.commit()
