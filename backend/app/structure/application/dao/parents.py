from abc import ABC, abstractmethod

from app.structure.domain.parent import Parent, ParentID


class IParentRepository(ABC):
    @abstractmethod
    async def get(self, ident: ParentID) -> Parent | None:
        raise NotImplementedError
