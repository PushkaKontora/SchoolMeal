from dataclasses import dataclass
from uuid import UUID, uuid4

from app.common.domain.authenticated_user import AuthenticatedUser
from app.feedbacks.application.repositories import ICanteenRepository, IFeedbackRepository
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.domain.text import FeedbackText


class CantLeaveFeedbackOnUnregisteredCanteen(Exception):
    pass


@dataclass
class FeedbackService:
    repository: IFeedbackRepository
    canteen_service: "CanteenService"

    async def leave_feedback_about_canteen(self, canteen_id: UUID, user: AuthenticatedUser, text: str) -> Feedback:
        """
        :raise CantLeaveFeedbackOnUnavailableCanteen: кухня не зарегистрирована
        :raise InsufficientMinLengthFeedbackText: не достигнута минимальная длина отзыва
        :raise ExceededMaxLengthFeedbackText: превышена максимальная длина отзыва
        """

        if not await self.canteen_service.is_canteen_registered(canteen_id):
            raise CantLeaveFeedbackOnUnregisteredCanteen

        feedback_text = FeedbackText(text)
        feedback = Feedback(
            id=uuid4(),
            canteen_id=canteen_id,
            user_id=user.id,
            text=feedback_text,
        )
        await self.repository.save(feedback)

        return feedback


@dataclass
class CanteenService:
    repository: ICanteenRepository

    async def is_canteen_registered(self, canteen_id: UUID) -> bool:
        return await self.repository.exists_by_id(canteen_id)
