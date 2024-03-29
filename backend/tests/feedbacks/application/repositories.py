from uuid import UUID

from app.feedbacks.application.repositories import ICanteensRepository, IFeedbacksRepository
from app.feedbacks.domain.canteen import Canteen
from app.feedbacks.domain.feedback import Feedback


class LocalFeedbacksRepository(IFeedbacksRepository):
    def __init__(self) -> None:
        self._feedbacks: list[Feedback] = []

    async def save(self, feedback: Feedback) -> None:
        self._feedbacks += [feedback]


class LocalCanteensRepository(ICanteensRepository):
    def __init__(self, canteens: list[Canteen] | None = None) -> None:
        self._canteens: list[Canteen] = canteens or []

    async def exists_by_id(self, canteen_id: UUID) -> bool:
        return any(canteen for canteen in self._canteens if canteen.id == canteen_id)
