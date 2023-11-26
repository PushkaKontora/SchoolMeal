from contextlib import nullcontext
from uuid import uuid4

import pytest

from app.children.application.repositories import IChildrenRepository, IParentsRepository, NotFoundChild, NotFoundParent
from app.children.application.use_cases import add_child_to_parent
from app.children.domain.child import Child
from app.children.domain.parent import ChildIsAlreadyAssignedToParent, Parent


async def test_adding_child(
    child: Child,
    parent: Parent,
    parents_repository: IParentsRepository,
    children_repository: IChildrenRepository,
):
    await add_child_to_parent(
        parent_id=parent.id,
        child_id=child.id.value,
        parents_repository=parents_repository,
        children_repository=children_repository,
    )


async def test_adding_unknown_child(
    parent: Parent,
    parents_repository: IParentsRepository,
    children_repository: IChildrenRepository,
):
    with pytest.raises(NotFoundChild):
        await add_child_to_parent(
            child_id="incorrect",
            parent_id=parent.id,
            parents_repository=parents_repository,
            children_repository=children_repository,
        )


async def test_adding_to_unknown_parent(
    child: Child,
    parents_repository: IParentsRepository,
    children_repository: IChildrenRepository,
):
    with pytest.raises(NotFoundParent):
        await add_child_to_parent(
            child_id=child.id.value,
            parent_id=uuid4(),
            parents_repository=parents_repository,
            children_repository=children_repository,
        )


async def test_adding_already_added_child(
    parent: Parent,
    child: Child,
    parents_repository: IParentsRepository,
    children_repository: IChildrenRepository,
):
    for i in range(2):
        error = pytest.raises(ChildIsAlreadyAssignedToParent) if i % 2 == 1 else nullcontext()

        with error:
            await add_child_to_parent(
                parent_id=parent.id,
                child_id=child.id.value,
                parents_repository=parents_repository,
                children_repository=children_repository,
            )
