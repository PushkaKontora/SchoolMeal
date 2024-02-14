from abc import ABC, abstractmethod

from app.nutrition.domain.pupil import Pupil, PupilID


class IPupilDAO(ABC):
    @abstractmethod
    async def update(self, pupil: Pupil) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id_: PupilID) -> Pupil | None:
        raise NotImplementedError
