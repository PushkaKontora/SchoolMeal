from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.feedbacks.api.v1.schemas import LeaveFeedbackAboutCanteenBody
from app.feedbacks.application import services
from app.feedbacks.application.dao.feedbacks import IFeedbackRepository
from app.feedbacks.domain.feedback import FeedbackText
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.shared.api import responses
from app.shared.api.errors import UnprocessableEntity
from app.shared.domain.user import UserID
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/feedbacks",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses=responses.UNPROCESSABLE_ENTITY,
)
@inject
async def leave_feedback_about_canteen(
    body: LeaveFeedbackAboutCanteenBody,
    authorized_user: AuthorizedUserDep,
    feedback_repository: IFeedbackRepository = Depends(Provide[FeedbacksContainer.feedback_repository]),
) -> OKSchema:
    try:
        user_id = UserID(authorized_user.id)
        text = FeedbackText(body.text)
    except ValueError as error:
        raise UnprocessableEntity(str(error)) from error

    await services.leave_feedback_about_canteen(user_id, text, feedback_repository)

    return OKSchema()
