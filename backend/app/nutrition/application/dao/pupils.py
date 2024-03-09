from abc import ABC, abstractmethod

from app.nutrition.domain.pupil import Pupil, PupilID
from app.shared.domain.school_class import ClassID
from app.shared.specifications import Specification


class PupilByIDs(Specification[Pupil]):
    def __init__(self, ids: set[PupilID]) -> None:
        self._ids = ids

    def is_satisfied_by(self, candidate: Pupil) -> bool:
        return candidate.id in self._ids


class PupilByClassID(Specification[Pupil]):
    def __init__(self, class_id: ClassID) -> None:
        self._class_id = class_id

    def is_satisfied_by(self, candidate: Pupil) -> bool:
        return candidate.class_id == self._class_id


class IPupilRepository(ABC):
    @abstractmethod
    async def merge(self, pupil: Pupil) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, ident: PupilID) -> Pupil | None:
        raise NotImplementedError

    @abstractmethod
    async def all(self, spec: Specification[Pupil] | None = None) -> list[Pupil]:
        raise NotImplementedError
