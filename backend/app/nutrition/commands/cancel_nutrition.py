from datetime import date

from app.nutrition.commands.context import NutritionContext
from app.nutrition.domain.periods import CancellationPeriod, Reason
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class CancelNutritionCommand(Command):
    pupil_id: str
    starts_at: date
    ends_at: date
    reason: str | None


class CancelNutritionCommandHandler(ICommandHandler[CancelNutritionCommand]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CancelNutritionCommand) -> None:
        """
        :raise NotFoundPupil: не найден ученик
        :raise SpecifiedReasonCannotBeEmpty: текст причины не может быть пустым
        :raise ExceededMaxLengthReason: превышена максимальная длина текста причины
        :raise EndCannotBeGreaterThanStart: дата начала периода больше, чем конечная дата
        """

        async with self._unit_of_work as context:
            pupil = await context.pupils.get_by_id(pupil_id=command.pupil_id)

            reasons = {Reason(command.reason)} if command.reason is not None else {}
            period = CancellationPeriod(
                starts_at=command.starts_at, ends_at=command.ends_at, reasons=frozenset(reasons)
            )
            pupil.cancel_nutrition(period)

            await context.pupils.update(pupil)

            await self._unit_of_work.commit()
