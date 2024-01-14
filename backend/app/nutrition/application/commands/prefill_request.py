from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.repositories import NotFoundDraftRequest
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import MealPlan, PupilID
from app.nutrition.domain.request import DraftRequest
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
        :raise RequestCannotBeUpdatedAfter: заявка не может быть отредактирована
        """

        async with self._unit_of_work as context:
            try:
                draft = await context.draft_requests.get_by_class_id_and_date(
                    class_id=command.class_id, on_date=Day(command.on_date)
                )
            except NotFoundDraftRequest:
                school_class = await context.school_classes.get_by_id(id_=command.class_id)
                draft = DraftRequest.prefill(school_class, on_date=Day(command.on_date))

            draft.edit(
                pupils={
                    PupilID(pupil.id): MealPlan(breakfast=pupil.breakfast, dinner=pupil.dinner, snacks=pupil.snacks)
                    for pupil in command.overriden_pupils
                }
            )
            await context.draft_requests.upsert(draft)

            await self._unit_of_work.commit()
