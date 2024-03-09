from abc import ABC, abstractmethod
from datetime import date

from app.nutrition.domain.request import Request, RequestStatus
from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification


class RequestByDate(Specification[Request]):
    def __init__(self, on_date: date) -> None:
        self._on_date = on_date

    def is_satisfied_by(self, candidate: Request) -> bool:
        return candidate.on_date == self._on_date


class RequestByStatus(Specification[Request]):
    def __init__(self, status: RequestStatus) -> None:
        self._status = status

    def is_satisfied_by(self, candidate: Request) -> bool:
        return candidate.status == self._status


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

    @abstractmethod
    async def get(self, class_id: ClassID, on_date: date) -> Request | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, spec: Specification[Request] | None = None) -> list[Request]:
        raise NotImplementedError
