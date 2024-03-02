from uuid import UUID

from result import Err, Ok, Result

from app.feedbacks.application.dao import IFeedbackRepository
from app.feedbacks.application.services import leave_feedback_about_work_of_canteen
from app.feedbacks.domain.feedback import FeedbackText, UserID
from app.ipc.feedbacks.api import IFeedbacksAPI


class FeedbacksAPI(IFeedbacksAPI):
    def __init__(self, feedback_repository: IFeedbackRepository) -> None:
        self._feedback_repository = feedback_repository

    async def leave_feedback_about_canteen(self, user_id: UUID, text: str) -> Result[None, str]:
        try:
            user_id_ = UserID(user_id)
            text_ = FeedbackText(text)
        except ValueError as error:
            return Err(str(error))

        leaving = await leave_feedback_about_work_of_canteen(user_id_, text_, self._feedback_repository)

        return Ok(leaving.unwrap())
