from abc import ABC, abstractmethod

from app.database.specifications import FilterSpecification
from app.users.domain.entities import User


class IUsersRepository(ABC):
    @abstractmethod
    async def get_one(self, specification: FilterSpecification) -> User | None:
        raise NotImplementedError
