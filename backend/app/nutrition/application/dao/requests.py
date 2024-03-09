from abc import ABC, abstractmethod
from datetime import date

from app.nutrition.domain.request import Request
from app.shared.domain.school_class import ClassID


class IRequestRepository(ABC):
    @abstractmethod
    async def add(self, request: Request) -> None:
        raise NotImplementedError

    @abstractmethod
    async def merge(self, request: Request) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists(self, class_id: ClassID, on_date: date) -> bool:
        raise NotImplementedError
