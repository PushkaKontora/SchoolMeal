from abc import ABC, abstractmethod

from app.shared.domain.pupil import PupilID
from app.shared.specifications import Specification
from app.structure.domain.parent import ParentID
from app.structure.domain.pupil import Pupil


class PupilByIDs(Specification[Pupil]):
    def __init__(self, ids: set[PupilID]) -> None:
        self._ids = ids

    def is_satisfied_by(self, candidate: Pupil) -> bool:
        return candidate.id in self._ids


class PupilByParentID(Specification[Pupil]):
    def __init__(self, parent_id: ParentID) -> None:
        self._parent_id = parent_id

    def is_satisfied_by(self, candidate: Pupil) -> bool:
        return self._parent_id in candidate.parent_ids


class IPupilRepository(ABC):
    @abstractmethod
    async def all(self, spec: Specification[Pupil] | None = None) -> list[Pupil]:
        raise NotImplementedError

    @abstractmethod
    async def get(self, ident: PupilID) -> Pupil | None:
        raise NotImplementedError

    @abstractmethod
    async def merge(self, pupil: Pupil) -> None:
        raise NotImplementedError
