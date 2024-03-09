import pytest

from app.shared.domain.personal_info import FullName
from app.shared.domain.pupil import PupilID
from app.shared.domain.school_class import ClassID
from app.structure.domain.parent import Parent, ParentID
from app.structure.domain.pupil import Pupil
from app.structure.domain.school_class import Literal, Number, SchoolClass
from app.structure.domain.teacher import Teacher, TeacherID


@pytest.fixture
def teacher() -> Teacher:
    return Teacher(id=TeacherID.generate())


@pytest.fixture
def school_class(teacher: Teacher) -> SchoolClass:
    return SchoolClass(id=ClassID.generate(), teacher_id=teacher.id, number=Number(1), literal=Literal("И"))


@pytest.fixture
def pupil(school_class: SchoolClass) -> Pupil:
    return Pupil(
        id=PupilID.generate(), name=FullName.create("Петров", "Василий"), class_id=school_class.id, parent_ids=set()
    )


@pytest.fixture
def parent() -> Parent:
    return Parent(id=ParentID.generate())
