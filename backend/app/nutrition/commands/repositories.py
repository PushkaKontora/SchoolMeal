from abc import ABC, abstractmethod
from uuid import UUID

from app.nutrition.domain.parent import Parent
from app.nutrition.domain.pupil import Pupil


class NotFoundPupil(Exception):
    pass


class NotFoundParent(Exception):
    pass


class NotFoundSchool(Exception):
    pass


class IPupilsRepository(ABC):
    @abstractmethod
    async def get_by_id(self, pupil_id: str) -> Pupil:
        """
        :raise NotFoundPupil: не найден ученик
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, pupil: Pupil) -> None:
        raise NotImplementedError


class IParentsRepository(ABC):
    @abstractmethod
    async def get_by_id(self, parent_id: UUID) -> Parent:
        """
        :raise NotFoundParent: не найден родитель
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, parent: Parent) -> None:
        raise NotImplementedError
