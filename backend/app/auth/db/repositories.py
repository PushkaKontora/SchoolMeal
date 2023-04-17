from abc import ABC, abstractmethod

from app.auth.domain.entities import IssuedToken, Password
from app.database.specifications import FilterSpecification


class IPasswordsRepository(ABC):
    @abstractmethod
    async def get_last(self, specification: FilterSpecification) -> Password | None:
        raise NotImplementedError


class IIssuedTokensRepository(ABC):
    @abstractmethod
    async def find_one(self, specification: FilterSpecification) -> IssuedToken | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, user_id: int, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def revoke(self, specification: FilterSpecification) -> None:
        pass
