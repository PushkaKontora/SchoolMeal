from uuid import uuid4

import pytest

from app.common.domain.authenticated_user import AuthenticatedUser
from app.feedbacks.application.services import CantLeaveFeedbackOnUnregisteredCanteen, FeedbackService
from app.feedbacks.domain.canteen import Canteen


async def test_leave_feedback_on_canteen(
    canteen: Canteen, authenticated_user: AuthenticatedUser, feedback_service: FeedbackService
):
    text = "Очень полезный отзыв"

    feedback = await feedback_service.leave_feedback_about_canteen(
        canteen_id=canteen.id, user=authenticated_user, text=text
    )

    assert feedback.canteen_id == canteen.id
    assert feedback.user_id == authenticated_user.id
    assert feedback.text.value == text


async def test_leave_feedback_on_unregistered_canteen(
    authenticated_user: AuthenticatedUser, feedback_service: FeedbackService
):
    with pytest.raises(CantLeaveFeedbackOnUnregisteredCanteen):
        await feedback_service.leave_feedback_about_canteen(
            canteen_id=uuid4(), user=authenticated_user, text="Очень полезный отзыв"
        )
