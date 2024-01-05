from datetime import date

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.dto import CancellationPeriodOut
from app.nutrition.domain.periods import CancellationPeriod, Reason
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class CancelNutritionCommand(Command):
    pupil_id: str
    starts_at: date
    ends_at: date
    reason: str | None


class CancelNutritionCommandHandler(ICommandHandler[CancelNutritionCommand, list[CancellationPeriodOut]]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: CancelNutritionCommand) -> list[CancellationPeriodOut]:
        """
        :raise NotFoundPupil: не найден ученик
        :raise SpecifiedReasonCannotBeEmpty: текст причины не может быть пустым
        :raise ExceededMaxLengthReason: превышена максимальная длина текста причины
        :raise EndCannotBeGreaterThanStart: дата начала периода больше, чем конечная дата
        :raise CannotCancelNutritionAfterTime: нельзя снимать с питания после 10 утра по ЕКБ
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

        return list(map(CancellationPeriodOut.from_model, pupil.cancellation_periods))
