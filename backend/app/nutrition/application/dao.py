from abc import ABC, abstractmethod

from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request
from app.nutrition.domain.school_class import ClassID, SchoolClass


class IPupilDAO(ABC):
    @abstractmethod
    async def update(self, pupil: Pupil) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: PupilID) -> Pupil | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_class_id(self, class_id: ClassID) -> list[Pupil]:
        raise NotImplementedError


class ISchoolClassDAO(ABC):
    @abstractmethod
    async def get_by_id(self, id_: ClassID) -> SchoolClass | None:
        raise NotImplementedError


class IRequestDAO(ABC):
    @abstractmethod
    async def upsert(self, request: Request) -> None:
        raise NotImplementedError
