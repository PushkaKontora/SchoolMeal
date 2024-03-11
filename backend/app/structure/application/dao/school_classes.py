from abc import ABC, abstractmethod

from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification
from app.structure.domain.school_class import Number, SchoolClass
from app.structure.domain.teacher import TeacherID


class ClassByIDs(Specification[SchoolClass]):
    def __init__(self, ids: set[ClassID]) -> None:
        self._ids = ids

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return candidate.id in self._ids


class ClassByTeacherID(Specification[SchoolClass]):
    def __init__(self, teacher_id: TeacherID) -> None:
        self._teacher_id = teacher_id

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return candidate.teacher_id == self._teacher_id


class ClassByNumberRange(Specification[SchoolClass]):
    def __init__(self, start: Number, end: Number) -> None:
        self._start = start
        self._end = end

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return self._start <= candidate.number <= self._end


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def all(self, spec: Specification[SchoolClass] | None = None) -> list[SchoolClass]:
        raise NotImplementedError