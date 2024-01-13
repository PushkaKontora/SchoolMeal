from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from app.nutrition.domain.menu import Menu
from app.nutrition.domain.parent import Parent
from app.nutrition.domain.periods import Day
from app.nutrition.domain.pupil import Pupil
from app.nutrition.domain.request import Request
from app.nutrition.domain.school_class import SchoolClass, SchoolClassType


class NotFoundPupil(Exception):
    pass


class NotFoundParent(Exception):
    pass


class NotFoundSchool(Exception):
    pass


class NotFoundSchoolClass(Exception):
    pass


class NotFoundMenu(Exception):
    pass


class NotFoundRequest(Exception):
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

    @abstractmethod
    async def get_by_class_id(self, class_id: UUID) -> list[Pupil]:
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


class IMenusRepository(ABC):
    @abstractmethod
    async def get_by_class_type_and_date(self, school_class_type: SchoolClassType, on_date: date) -> Menu:
        """
        :raise NotFoundMenu: не найдено меню
        """
        raise NotImplementedError


class ISchoolClassesRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UUID) -> SchoolClass:
        """
        :raise NotFoundSchoolClass: не найден класс
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_teacher_id(self, teacher_id: UUID) -> list[SchoolClass]:
        raise NotImplementedError


class IRequestsRepository(ABC):
    @abstractmethod
    async def get_by_class_id_and_date(self, class_id: UUID, on_date: Day) -> Request:
        """
        :raise NotFoundRequest: не найдена заявка для класса на дату
        """
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, request: Request) -> None:
        raise NotImplementedError
