from uuid import UUID, uuid4

from app.feedbacks.application.repositories import ICanteensRepository, IFeedbacksRepository
from app.feedbacks.domain.feedback import Feedback
from app.feedbacks.domain.text import FeedbackText
from app.shared.unit_of_work import UnitOfWork


class CantLeaveFeedbackOnUnregisteredCanteen(Exception):
    pass


class FeedbacksService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        feedbacks_repository: IFeedbacksRepository,
        canteens_repository: ICanteensRepository,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._feedbacks = feedbacks_repository
        self._canteens = canteens_repository

    async def leave_feedback_about_canteen(self, canteen_id: UUID, user_id: UUID, text: str) -> Feedback:
        """
        :raise CantLeaveFeedbackOnUnavailableCanteen: кухня не зарегистрирована
        :raise InsufficientMinLengthFeedbackText: не достигнута минимальная длина отзыва
        :raise ExceededMaxLengthFeedbackText: превышена максимальная длина отзыва
        """

        async with self._unit_of_work as session:
            if not await self._canteens.exists_by_id(canteen_id):
                raise CantLeaveFeedbackOnUnregisteredCanteen

            feedback_text = FeedbackText(text)
            feedback = Feedback(
                id=uuid4(),
                canteen_id=canteen_id,
                user_id=user_id,
                text=feedback_text,
            )
            await self._feedbacks.save(feedback)

            await session.commit()

        return feedback
