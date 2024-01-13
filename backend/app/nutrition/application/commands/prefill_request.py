from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.repositories import NotFoundRequest
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan, PupilID
from app.nutrition.domain.request import Request
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.unit_of_work.abc import IUnitOfWork


class OverridenPupil(BaseModel):
    id: str
    breakfast: bool
    dinner: bool
    snacks: bool


class PrefillRequestCommand(Command):
    class_id: UUID
    on_date: date
    overriden_pupils: list[OverridenPupil] = []


class PrefillRequestCommandHandler(ICommandHandler[PrefillRequestCommand, None]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: PrefillRequestCommand) -> None:
        """
        :raise NotFoundSchoolClass: не найден класс по идентификатору
        :raise RequestIsAlreadyToBeSubmitted: заявка уже готова к отправке и не может быть изменена
        """

        async with self._unit_of_work as context:
            try:
                request = await context.requests.get_by_class_id_and_date(
                    class_id=command.class_id, on_date=Day(command.on_date)
                )
            except NotFoundRequest:
                school_class = await context.school_classes.get_by_id(id_=command.class_id)
                request = Request.prefill(school_class, on_date=Day(command.on_date))

            request.prepare(
                pupils={
                    PupilID(pupil.id): MealPlan(breakfast=pupil.breakfast, dinner=pupil.dinner, snacks=pupil.snacks)
                    for pupil in command.overriden_pupils
                }
            )
            await context.requests.upsert(request)

            await self._unit_of_work.commit()
