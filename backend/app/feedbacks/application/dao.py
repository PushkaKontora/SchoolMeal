from abc import ABC, abstractmethod

from app.feedbacks.domain.feedback import Feedback


class IFeedbackRepository(ABC):
    @abstractmethod
    async def add(self, feedback: Feedback) -> None:
        raise NotImplementedError
