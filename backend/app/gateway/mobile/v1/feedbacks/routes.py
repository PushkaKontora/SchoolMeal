from fastapi import APIRouter, status
from result import Err

from app.feedbacks.api import handlers as feedbacks_api
from app.gateway import responses
from app.gateway.errors import UnprocessableEntity
from app.gateway.mobile.v1.feedbacks.dto import LeaveFeedbackAboutCanteenBody
from app.shared.api.errors import DomainValidationError
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/feedbacks",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses=responses.UNPROCESSABLE_ENTITY,
)
async def leave_feedback_about_canteen(
    body: LeaveFeedbackAboutCanteenBody, authorized_user: AuthorizedUserDep
) -> OKSchema:
    match await feedbacks_api.leave_feedback_about_canteen(user_id=authorized_user.id, text=body.text):
        case Err(DomainValidationError(message=message)):
            raise UnprocessableEntity(message)

    return OKSchema()
