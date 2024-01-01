from uuid import UUID

from pydantic.dataclasses import dataclass

from app.children.domain.child import Child, ChildID
from app.shared.domain import Entity


class ChildIsAlreadyAssignedToParent(Exception):
    pass


@dataclass
class Parent(Entity):
    id: UUID
    child_ids: set[ChildID]

    def add_child(self, child: Child) -> "Parent":
        """
        :raise ChildIsAlreadyAssignedToParent: ребёнок уже привязан к родителю
        """

        if child.id in self.child_ids:
            raise ChildIsAlreadyAssignedToParent

        self.child_ids.add(child.id)
        return self
