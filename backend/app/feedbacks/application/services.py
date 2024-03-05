from result import Ok, Result

from app.feedbacks.application.dao import IFeedbackRepository
from app.feedbacks.domain.feedback import Feedback, FeedbackText, UserID


async def leave_feedback_about_canteen(
    user_id: UserID, text: FeedbackText, feedback_repository: IFeedbackRepository
) -> Result[None, None]:
    leaving = Feedback.leave_about_work_of_canteen(user_id, text)

    await feedback_repository.add(feedback=leaving.unwrap())

    return Ok(None)
