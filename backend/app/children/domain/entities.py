from datetime import date, datetime

from app.utils.entity import Entity


class ChildIn(Entity):
    child_id: str


class PeriodOut(Entity):
    id: int
    start_date: date
    end_date: date | None
    comment: str


class TeacherOut(Entity):
    id: int
    last_name: str
    first_name: str
    phone: str
    email: str


class SchoolOut(Entity):
    id: int
    name: str


class ClassOut(Entity):
    id: int
    number: int
    letter: str
    has_breakfast: bool
    has_lunch: bool
    has_dinner: bool
    teachers: list[TeacherOut]
    school: SchoolOut


class ChildOut(Entity):
    id: str
    last_name: str
    first_name: str
    certificate_before_date: datetime | None
    balance: float
    breakfast: bool
    lunch: bool
    dinner: bool
    school_class: ClassOut | None
    cancel_meal_periods: list[PeriodOut]


class PlanIn(Entity):
    breakfast: bool | None = None
    lunch: bool | None = None
    dinner: bool | None = None


class PlanOut(Entity):
    breakfast: bool
    lunch: bool
    dinner: bool
