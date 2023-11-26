from uuid import UUID

from app.children.application.repositories import IChildrenRepository, IParentsRepository, NotFoundChild, NotFoundParent
from app.children.domain.child import Child, ChildID
from app.children.domain.parent import Parent


class LocalParentsRepository(IParentsRepository):
    def __init__(self, parents: list[Parent] | None = None) -> None:
        self._parent_ids: dict[UUID, Parent] = {parent.id: parent for parent in parents or []}

    async def get_by_id(self, parent_id: UUID) -> Parent:
        try:
            return self._parent_ids[parent_id]
        except KeyError as error:
            raise NotFoundParent from error

    async def update(self, parent: Parent) -> None:
        if parent.id not in self._parent_ids:
            return

        self._parent_ids[parent.id] = parent


class LocalChildrenRepository(IChildrenRepository):
    def __init__(self, children: list[Child] | None = None) -> None:
        self._child_ids: dict[ChildID, Child] = {child.id: child for child in children}

    async def get_by_id(self, child_id: ChildID) -> Child:
        try:
            return self._child_ids[child_id]
        except KeyError as error:
            raise NotFoundChild from error

    async def get_all_by_ids(self, ids: set[ChildID]) -> list[Child]:
        return list(filter(bool, [self._child_ids.get(child_id, None) for child_id in ids]))
