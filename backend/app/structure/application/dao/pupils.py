from abc import ABC, abstractmethod

from app.shared.domain.pupil import PupilID
from app.structure.domain.pupil import Pupil


class IPupilRepository(ABC):
    @abstractmethod
    async def get(self, ident: PupilID) -> Pupil | None:
        raise NotImplementedError

    @abstractmethod
    async def merge(self, pupil: Pupil) -> None:
        raise NotImplementedError
