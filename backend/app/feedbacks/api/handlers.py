from uuid import UUID

from result import Err, Ok, Result

from app.feedbacks.application import services
from app.feedbacks.domain.feedback import FeedbackText, UserID
from app.shared.api.errors import DomainValidationError


async def leave_feedback_about_canteen(user_id: UUID, text: str) -> Result[None, DomainValidationError]:
    try:
        feedback_text = FeedbackText(text)
    except ValueError as error:
        return Err(DomainValidationError(message=str(error)))

    result = await services.leave_feedback_about_canteen(user_id=UserID(user_id), text=feedback_text)

    return Ok(result.unwrap())
