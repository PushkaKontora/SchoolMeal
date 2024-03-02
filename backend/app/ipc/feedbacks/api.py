from abc import ABC, abstractmethod
from uuid import UUID

from result import Result


class IFeedbacksAPI(ABC):
    @abstractmethod
    async def leave_feedback_about_canteen(self, user_id: UUID, text: str) -> Result[None, str]:
        raise NotImplementedError
