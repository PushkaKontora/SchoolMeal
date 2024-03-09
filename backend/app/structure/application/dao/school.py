from abc import ABC, abstractmethod

from app.structure.domain.school import School


class ISchoolDAO(ABC):
    @abstractmethod
    async def get(self) -> School:
        raise NotImplementedError
