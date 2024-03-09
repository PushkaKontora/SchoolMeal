from abc import ABC, abstractmethod

from app.nutrition.domain.school_class import SchoolClass
from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def get(self, ident: ClassID) -> SchoolClass | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, spec: Specification[SchoolClass] | None = None) -> list[SchoolClass]:
        raise NotImplementedError
