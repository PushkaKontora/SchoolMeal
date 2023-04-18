from abc import ABC, abstractmethod

from app.auth.db.models import IssuedToken, Password
from app.database.base import Repository
from app.database.specifications import FilterSpecification


class BasePasswordsRepository(Repository[Password], ABC):
    @abstractmethod
    async def get_last(self, specification: FilterSpecification) -> Password | None:
        raise NotImplementedError


class BaseIssuedTokensRepository(Repository[IssuedToken], ABC):
    @abstractmethod
    async def revoke(self, specification: FilterSpecification) -> None:
        raise NotImplementedError