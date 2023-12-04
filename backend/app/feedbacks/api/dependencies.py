from typing import Annotated

from fastapi import Depends

from app.feedbacks.application.repositories import ICanteenRepository, IFeedbackRepository
from app.feedbacks.application.services import CanteenService, FeedbackService
from app.feedbacks.infrastructure.db.repositories import CanteenRepository, FeedbackRepository
from app.shared.fastapi.dependencies.db import SessionDep


def _get_feedback_repository(session: SessionDep) -> IFeedbackRepository:
    return FeedbackRepository(session)


def _get_canteen_repository(session: SessionDep) -> ICanteenRepository:
    return CanteenRepository(session)


def _get_canteen_service(canteen_repository: ICanteenRepository = Depends(_get_canteen_repository)) -> CanteenService:
    return CanteenService(repository=canteen_repository)


def _get_feedback_service(
    feedback_repository: IFeedbackRepository = Depends(_get_feedback_repository),
    canteen_service: CanteenService = Depends(_get_canteen_service),
) -> FeedbackService:
    return FeedbackService(repository=feedback_repository, canteen_service=canteen_service)


FeedbackServiceDep = Annotated[FeedbackService, Depends(_get_feedback_service)]
