from app.structure.domain.parent import Parent
from app.structure.domain.pupil import Pupil


def test_attaching_pupil_to_parent(pupil: Pupil, parent: Parent) -> None:
    assert pupil.attach_to_parent(parent).is_ok()
    assert len(pupil.parents) == 1

    assert pupil.attach_to_parent(parent).is_err()
    assert len(pupil.parents) == 1
