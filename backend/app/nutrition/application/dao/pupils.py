from abc import ABC, abstractmethod

from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID
from app.shared.specification import Specification


class Filter(Specification[Pupil], ABC):
    pass


class PupilByClassID(Filter):
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
    async def all(self, spec: Filter) -> list[Pupil]:
        raise NotImplementedError
