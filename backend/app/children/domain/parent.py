from uuid import UUID

from pydantic import BaseModel

from app.children.domain.child import Child, ChildID


class ChildIsAlreadyAssignedToParent(Exception):
    pass


class Parent(BaseModel):
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
