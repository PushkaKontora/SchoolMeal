from fastapi import APIRouter, status
from pydantic import BaseModel
from result import as_result

from app.feedbacks.application import services
from app.feedbacks.domain.feedback import FeedbackText, UserID
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import UnprocessableEntity
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


class FeedbackTextIn(BaseModel):
    text: str


@router.post(
    "/feedbacks/work-of-canteen",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses=responses.UNPROCESSABLE_ENTITY,
)
async def leave_feedback_about_work_of_canteen(body: FeedbackTextIn, authorized_user: AuthorizedUserDep) -> OKSchema:
    text = as_result(ValueError)(lambda x: FeedbackText(x))(body.text).unwrap_or_raise(UnprocessableEntity)
    user_id = as_result(ValueError)(lambda x: UserID(x))(authorized_user.id).unwrap_or_raise(UnprocessableEntity)

    leaving = await services.leave_feedback_about_work_of_canteen(user_id, text)

    return leaving.map(lambda _: OKSchema()).unwrap()
