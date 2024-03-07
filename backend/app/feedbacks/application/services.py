from dependency_injector.wiring import Provide, inject
from result import Ok, Result

from app.feedbacks.application.dao.feedbacks import IFeedbackRepository
from app.feedbacks.domain.feedback import Feedback, FeedbackText, UserID
from app.feedbacks.infrastructure.dependencies import FeedbacksContainer


@inject
async def leave_feedback_about_canteen(
    user_id: UserID,
    text: FeedbackText,
    feedback_repository: IFeedbackRepository = Provide[FeedbacksContainer.feedback_repository],
) -> Result[None, None]:
    leaving = Feedback.leave_about_work_of_canteen(user_id, text)

    await feedback_repository.add(feedback=leaving.unwrap())

    return Ok(None)
