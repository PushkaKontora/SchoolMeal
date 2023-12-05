from abc import ABC, abstractmethod
from uuid import UUID

from app.feedbacks.domain.feedback import Feedback


class IFeedbacksRepository(ABC):
    @abstractmethod
    async def save(self, feedback: Feedback) -> None:
        raise NotImplementedError


class ICanteensRepository(ABC):
    @abstractmethod
    async def exists_by_id(self, canteen_id: UUID) -> bool:
        raise NotImplementedError
