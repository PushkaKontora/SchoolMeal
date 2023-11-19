from abc import ABC, abstractmethod

from app.nutrition.domain.pupil import Pupil, PupilID


class NotFoundPupil(Exception):
    pass


class IPupilsRepository(ABC):
    @abstractmethod
    async def get_by_id(self, pupil_id: PupilID) -> Pupil:
        """
        :raise NotFoundPupil:
        """
        raise NotImplementedError
