from app.nutrition.domain.parent import Parent
from app.nutrition.domain.pupil import Pupil


def test_attaching_child(parent: Parent, pupil: Pupil) -> None:
    assert parent.attach_child(pupil).is_ok()
    assert len(parent.children) == 1

    assert parent.attach_child(pupil).is_err()
    assert len(parent.children) == 1
