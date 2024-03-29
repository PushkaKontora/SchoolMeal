from uuid import uuid4

import pytest

from app.feedbacks.application.services import CantLeaveFeedbackOnUnregisteredCanteen, FeedbacksService
from app.feedbacks.domain.canteen import Canteen
from app.shared.fastapi.schemas import AuthorizedUser


async def test_leave_feedback_on_canteen(
    canteen: Canteen, authorized_user: AuthorizedUser, feedbacks_service: FeedbacksService
):
    text = "Очень полезный отзыв"

    feedback = await feedbacks_service.leave_feedback_about_canteen(
        canteen_id=canteen.id, user_id=authorized_user.id, text=text
    )

    assert feedback.canteen_id == canteen.id
    assert feedback.user_id == authorized_user.id
    assert feedback.text.value == text


async def test_leave_feedback_on_unregistered_canteen(
    authorized_user: AuthorizedUser, feedbacks_service: FeedbacksService
):
    with pytest.raises(CantLeaveFeedbackOnUnregisteredCanteen):
        await feedbacks_service.leave_feedback_about_canteen(
            canteen_id=uuid4(), user_id=authorized_user.id, text="Очень полезный отзыв"
        )
