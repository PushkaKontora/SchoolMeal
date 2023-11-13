import pytest

from app.children.domain.child import Child
from app.children.domain.parent import ChildIsAlreadyAssignedToParent, Parent


def test_add_child(child: Child, parent: Parent):
    parent.add_child(child)

    assert child.id in parent.child_ids


def test_assigning_to_parent_who_has_already_assigned(child: Child, parent: Parent):
    parent.add_child(child)

    with pytest.raises(ChildIsAlreadyAssignedToParent):
        parent.add_child(child)

    assert len(parent.child_ids) == 1
