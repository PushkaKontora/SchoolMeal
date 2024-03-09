from abc import ABC, abstractmethod

from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification
from app.structure.domain.school_class import SchoolClass


class ClassByIDs(Specification[SchoolClass]):
    def __init__(self, ids: set[ClassID]) -> None:
        self._ids = ids

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return candidate.id in self._ids


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def all(self, spec: Specification[SchoolClass] | None = None) -> list[SchoolClass]:
        raise NotImplementedError
