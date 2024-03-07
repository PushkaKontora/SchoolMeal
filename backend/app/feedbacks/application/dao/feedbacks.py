from abc import ABC, abstractmethod

from app.feedbacks.domain.feedback import Feedback
from app.shared.specification import Specification


class Filter(Specification[Feedback], ABC):
    pass


class IFeedbackRepository(ABC):
    @abstractmethod
    async def add(self, feedback: Feedback) -> None:
        raise NotImplementedError
