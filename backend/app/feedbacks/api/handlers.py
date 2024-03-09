from uuid import UUID

from dependency_injector.wiring import Provide, inject
from result import Err, Ok, Result

from app.feedbacks.application import services
from app.feedbacks.application.dao.feedbacks import IFeedbackRepository
from app.feedbacks.domain.feedback import FeedbackText
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer
from app.shared.api.errors import DomainValidationError
from app.shared.domain.user import UserID


@inject
async def leave_feedback_about_canteen(
    user_id: UUID, text: str, feedback_repository: IFeedbackRepository = Provide[FeedbacksContainer.feedback_repository]
) -> Result[None, DomainValidationError]:
    try:
        feedback_text = FeedbackText(text)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    result = await services.leave_feedback_about_canteen(
        user_id=UserID(user_id), text=feedback_text, feedback_repository=feedback_repository
    )

    return Ok(result.unwrap())
