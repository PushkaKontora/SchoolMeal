from datetime import datetime

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.repositories import NotFoundDraftRequest
from app.nutrition.domain.periods import Day
from app.nutrition.domain.request import DraftRequest
from app.nutrition.domain.services import submit_request
from app.shared.cqs.commands import Command, ICommandHandler
from app.shared.domain import timezones
from app.shared.unit_of_work.abc import IUnitOfWork


class SubmitRequestsCommand(Command):
    pass


class SubmitRequestsCommandHandler(ICommandHandler[SubmitRequestsCommand, None]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext]) -> None:
        self._unit_of_work = unit_of_work

    async def handle(self, command: SubmitRequestsCommand) -> None:
        now = Day(datetime.now(timezones.yekaterinburg).date())

        async with self._unit_of_work as context:
            for school_class in await context.school_classes.get_all():
                try:
                    draft = await context.draft_requests.get_by_class_id_and_date(class_id=school_class.id, on_date=now)
                except NotFoundDraftRequest:
                    draft = DraftRequest.prefill(school_class, on_date=now)

                request = submit_request(school_class, draft)
                await context.requests.save(request)

            await self._unit_of_work.commit()
