from fastapi import APIRouter, status
from pydantic import BaseModel

from app.feedbacks.application import commands
from app.feedbacks.domain.feedback import FeedbackText, UserID
from app.shared.exceptions import DomainException
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import UnprocessableEntityError
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
    try:
        text = FeedbackText(body.text)
        user_id = UserID(authorized_user.id)
    except DomainException as error:
        raise UnprocessableEntityError(error.message)

    leaving = await commands.leave_feedback_about_work_of_canteen(user_id, text)

    return leaving.map(lambda _: OKSchema()).unwrap()
