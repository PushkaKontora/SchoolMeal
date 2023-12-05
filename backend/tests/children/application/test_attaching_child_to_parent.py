from contextlib import nullcontext
from uuid import uuid4

import pytest

from app.children.application.repositories import NotFoundChild, NotFoundParent
from app.children.application.services import ChildrenService
from app.children.domain.child import Child
from app.children.domain.parent import ChildIsAlreadyAssignedToParent, Parent


async def test_attaching_unknown_child(parent: Parent, children_service: ChildrenService):
    with pytest.raises(NotFoundChild):
        await children_service.attach_child_to_parent(child_id="incorrect", parent_id=parent.id)


async def test_attaching_child_to_unknown_parent(child: Child, children_service: ChildrenService):
    with pytest.raises(NotFoundParent):
        await children_service.attach_child_to_parent(child_id=child.id.value, parent_id=uuid4())


async def test_reattaching(parent: Parent, child: Child, children_service: ChildrenService):
    for i in range(2):
        error = pytest.raises(ChildIsAlreadyAssignedToParent) if i % 2 == 1 else nullcontext()

        with error:
            await children_service.attach_child_to_parent(parent_id=parent.id, child_id=child.id.value)
