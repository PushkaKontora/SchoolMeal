from abc import ABC, abstractmethod

from app.nutrition.domain.school_class import ClassID, Number, SchoolClass
from app.nutrition.domain.teacher import TeacherID
from app.shared.specifications import Specification


class ClassByNumberRange(Specification[SchoolClass]):
    def __init__(self, start: Number, end: Number) -> None:
        self._start = start
        self._end = end

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return self._start <= candidate.number <= self._end


class ClassByTeacherID(Specification[SchoolClass]):
    def __init__(self, teacher_id: TeacherID) -> None:
        self._teacher_id = teacher_id

    def is_satisfied_by(self, candidate: SchoolClass) -> bool:
        return candidate.teacher_id == self._teacher_id


class ISchoolClassRepository(ABC):
    @abstractmethod
    async def get(self, ident: ClassID) -> SchoolClass | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, spec: Specification[SchoolClass] | None = None) -> list[SchoolClass]:
        raise NotImplementedError
