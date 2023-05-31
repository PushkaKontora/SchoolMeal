from app.schools.domain.entities import SchoolOut
from app.users.domain.entities import ContactOut
from app.utils.entity import Entity


class SchoolClassesGetOptions(Entity):
    teacher_id: int | None = None


class ClassOut(Entity):
    id: int
    number: int
    letter: str
    has_breakfast: bool
    has_lunch: bool
    has_dinner: bool
    school: SchoolOut


class ClassWithTeachersOut(ClassOut):
    teachers: list[ContactOut]
