from abc import ABC, abstractmethod

from app.nutrition.domain.parent import Parent, ParentID


class IParentRepository(ABC):
    @abstractmethod
    async def merge(self, parent: Parent) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, ident: ParentID) -> Parent | None:
        raise NotImplementedError
