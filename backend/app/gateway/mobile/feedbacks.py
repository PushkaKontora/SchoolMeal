from fastapi import APIRouter, status
from result import Ok, do

from app.gateway.dependencies import FeedbacksAPIDep
from app.gateway.mobile.dto import FeedbackTextIn
from app.shared.fastapi import responses
from app.shared.fastapi.dependencies.headers import AuthorizedUserDep
from app.shared.fastapi.errors import BadRequest
from app.shared.fastapi.schemas import OKSchema


router = APIRouter()


@router.post(
    "/feedbacks",
    summary="Оставить отзыв о столовой",
    status_code=status.HTTP_201_CREATED,
    responses=responses.BAD_REQUEST,
)
async def leave_feedback_about_canteen(
    body: FeedbackTextIn, authorized_user: AuthorizedUserDep, feedbacks_api: FeedbacksAPIDep
) -> OKSchema:
    return do(
        Ok(OKSchema())
        for _ in await feedbacks_api.leave_feedback_about_canteen(
            user_id=authorized_user.id,
            text=body.text,
        )
    ).unwrap_or_raise(BadRequest)
