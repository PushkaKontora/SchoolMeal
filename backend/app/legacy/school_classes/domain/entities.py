from app.legacy.schools.domain.entities import SchoolOut
from app.legacy.users.domain.entities import ContactOut
from app.legacy.utils.entity import Entity


class SchoolClassesGetOptions(Entity):
    teacher_id: int | None = None


class ClassOut(Entity):
    id: int
    number: int
    letter: str
    has_breakfast: bool
    has_lunch: bool
    has_dinner: bool


class ClassWithSchoolOut(ClassOut):
    school: SchoolOut


class ClassWithTeachersOut(ClassWithSchoolOut):
    teachers: list[ContactOut]
