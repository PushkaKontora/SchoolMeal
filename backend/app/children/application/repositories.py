from abc import ABC, abstractmethod
from uuid import UUID

from app.children.domain.child import Child, ChildID
from app.children.domain.parent import Parent


class NotFoundParent(Exception):
    pass


class NotFoundChild(Exception):
    pass


class IParentsRepository(ABC):
    @abstractmethod
    async def get_by_id(self, parent_id: UUID) -> Parent:
        """
        :raise NotFoundParent:
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, parent: Parent) -> None:
        raise NotImplementedError


class IChildrenRepository(ABC):
    @abstractmethod
    async def get_by_id(self, child_id: ChildID) -> Child:
        """
        :raise NotFoundChild:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all_by_ids(self, ids: set[ChildID]) -> list[Child]:
        raise NotImplementedError
