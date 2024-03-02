import pytest

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.parent import Parent, ParentID
from app.nutrition.domain.personal_info import Email, FullName, Phone
from app.nutrition.domain.pupil import Pupil, PupilID
from app.nutrition.domain.school_class import ClassID, Literal, Number, SchoolClass
from app.nutrition.domain.teacher import Teacher, TeacherID
from app.nutrition.domain.times import Timeline


@pytest.fixture
def parent() -> Parent:
    return Parent(
        id=ParentID.generate(),
        name=FullName.create("Дыков", "Лима"),
        email=Email("peroovy@gmail.com"),
        phone=Phone("8005553535"),
        children=set(),
    )


@pytest.fixture
def teacher() -> Teacher:
    return Teacher(id=TeacherID.generate(), name=FullName.create(last="Петров", first="Василий"))


@pytest.fixture
def school_class(teacher: Teacher) -> SchoolClass:
    return SchoolClass(
        id=ClassID.generate(),
        teacher_id=teacher.id,
        number=Number(11),
        literal=Literal("И"),
        mealtimes={Mealtime.DINNER},
    )


@pytest.fixture
def pupil(school_class: SchoolClass) -> Pupil:
    return Pupil(
        id=PupilID.generate(),
        class_id=school_class.id,
        name=FullName.create("Юеров", "Прий"),
        mealtimes={Mealtime.DINNER},
        preferential_until=None,
        cancellation=Timeline(),
    )
