import pytest

from app.nutrition.domain.parent import ChildIsAlreadyAttachedToParent, Parent
from app.nutrition.domain.pupil import Pupil


def test_add_child(parent: Parent, pupil: Pupil):
    parent.add_child(pupil)

    assert pupil.id in parent.child_ids


def test_assigning_to_parent_who_has_already_assigned(parent: Parent, pupil: Pupil):
    parent.add_child(pupil)

    with pytest.raises(ChildIsAlreadyAttachedToParent):
        parent.add_child(pupil)

    assert len(parent.child_ids) == 1
