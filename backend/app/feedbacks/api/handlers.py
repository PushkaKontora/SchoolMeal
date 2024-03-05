from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.feedbacks.api.dto import LeaveFeedbackAboutCanteenIn
from app.feedbacks.application import services
from app.feedbacks.application.dao import IFeedbackRepository
from app.feedbacks.domain.feedback import FeedbackText, UserID
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.shared.api.errors import ValidationError


@inject
async def leave_feedback_about_canteen(
    command: LeaveFeedbackAboutCanteenIn,
    feedback_repository: IFeedbackRepository = Provide[FeedbacksContainer.feedback_repository],
) -> Result[None, ValidationError]:
    try:
        user_id = UserID(command.user_id)
        text = FeedbackText(command.text)
    except ValueError as error:
        return Err(ValidationError(str(error)))

    result = await services.leave_feedback_about_canteen(user_id, text, feedback_repository)

    return Ok(result.unwrap())
