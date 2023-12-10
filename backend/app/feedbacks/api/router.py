from uuid import UUID

from fastapi import APIRouter, status

from app.common.api import responses
from app.common.api.dependencies.db import SessionDep
from app.common.api.dependencies.headers import AuthorizedUserDep
from app.common.api.errors import NotFoundError, UnprocessableEntityError
from app.common.api.schemas import OKSchema
from app.feedbacks.api.dependencies import FeedbackServiceDep
from app.feedbacks.api.schemas import FeedbackIn
from app.feedbacks.application.services import CantLeaveFeedbackOnUnregisteredCanteen
from app.feedbacks.domain.text import ExceededMaxLengthFeedbackText, InsufficientMinLengthFeedbackText


router = APIRouter(prefix="/canteens/{canteen_id}", tags=["Отзывы столовой"])


@router.post(
    "/feedbacks",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses=responses.UNPROCESSABLE_ENTITY | responses.NOT_FOUND,
)
async def leave_feedback_about_canteen(
    canteen_id: UUID,
    feedback: FeedbackIn,
    session: SessionDep,
    authorized_user: AuthorizedUserDep,
    feedback_service: FeedbackServiceDep,
) -> OKSchema:
    try:
        async with session.begin():
            await feedback_service.leave_feedback_about_canteen(
                canteen_id=canteen_id, user_id=authorized_user.id, text=feedback.text
            )

    except InsufficientMinLengthFeedbackText as error:
        raise UnprocessableEntityError("Отзыв не может быть пустым") from error

    except ExceededMaxLengthFeedbackText as error:
        raise UnprocessableEntityError("Превышена максимальная длина отзыва") from error

    except CantLeaveFeedbackOnUnregisteredCanteen as error:
        raise NotFoundError("Кухня не зарегистрирована в системе") from error

    return OKSchema(detail="Отзыв успешно отправлен")
