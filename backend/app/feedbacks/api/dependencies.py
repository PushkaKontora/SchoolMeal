from typing import Annotated

from fastapi import Depends

from app.feedbacks.application.services import FeedbacksService
from app.feedbacks.infrastructure.db.repositories import CanteensRepository, FeedbacksRepository
from app.shared.fastapi.dependencies.db import SessionDep
from app.shared.fastapi.dependencies.unit_of_work import UnitOfWorkDep


def _get_feedbacks_service(session: SessionDep, unit_of_work: UnitOfWorkDep) -> FeedbacksService:
    return FeedbacksService(
        unit_of_work=unit_of_work,
        feedbacks_repository=FeedbacksRepository(session),
        canteens_repository=CanteensRepository(session),
    )


FeedbacksServiceDep = Annotated[FeedbacksService, Depends(_get_feedbacks_service)]
