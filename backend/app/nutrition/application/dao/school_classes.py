from abc import ABC, abstractmethod

from app.nutrition.domain.school_class import ClassID, SchoolClass
from app.shared.specification import Specification


class Filter(Specification[SchoolClass], ABC):
    pass


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def get(self, ident: ClassID) -> SchoolClass | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, spec: Filter | None = None) -> list[SchoolClass]:
        raise NotImplementedError
