from uuid import UUID

from fastapi import APIRouter, status

from app.common.api.dependencies.db import SessionDep
from app.common.api.dependencies.headers import AuthenticatedUserDep
from app.common.api.errors import NotFoundError, UnprocessableEntity
from app.common.api.schemas import HTTPError, OKSchema
from app.feedbacks.api.dependencies import FeedbackServiceDep
from app.feedbacks.api.schemas import FeedbackIn
from app.feedbacks.application.services import CantLeaveFeedbackOnUnregisteredCanteen
from app.feedbacks.domain.text import ExceededMaxLengthFeedbackText, InsufficientMinLengthFeedbackText


router = APIRouter()


@router.post(
    "/feedbacks",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError},
    },
)
async def leave_feedback_about_canteen(
    canteen_id: UUID,
    feedback: FeedbackIn,
    session: SessionDep,
    authenticated_user: AuthenticatedUserDep,
    feedback_service: FeedbackServiceDep,
) -> OKSchema:
    try:
        async with session.begin():
            await feedback_service.leave_feedback_about_canteen(
                canteen_id=canteen_id, user=authenticated_user, text=feedback.text
            )

    except InsufficientMinLengthFeedbackText as error:
        raise UnprocessableEntity(detail="Отзыв не может быть пустым") from error

    except ExceededMaxLengthFeedbackText as error:
        raise UnprocessableEntity(detail="Превышена максимальная длина отзыва") from error

    except CantLeaveFeedbackOnUnregisteredCanteen as error:
        raise NotFoundError(detail="Кухня не зарегистрирована в системе") from error

    return OKSchema(detail="Отзыв успешно отправлен")
