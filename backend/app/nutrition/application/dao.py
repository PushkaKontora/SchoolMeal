from abc import ABC, abstractmethod

from app.nutrition.domain.parent import Parent, ParentID
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.request import Request
from app.nutrition.domain.school_class import ClassID, SchoolClass


class IPupilRepository(ABC):
    @abstractmethod
    async def merge(self, pupil: Pupil) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: PupilID) -> Pupil | None:
        raise NotImplementedError

    @abstractmethod
    async def all_by_class_id(self, class_id: ClassID) -> list[Pupil]:
        raise NotImplementedError


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: ClassID) -> SchoolClass | None:
        raise NotImplementedError


class IRequestRepository(ABC):
    @abstractmethod
    async def merge(self, request: Request) -> None:
        raise NotImplementedError


class IParentRepository(ABC):
    @abstractmethod
    async def merge(self, parent: Parent) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: ParentID) -> Parent | None:
        raise NotImplementedError
