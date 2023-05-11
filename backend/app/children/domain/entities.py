from datetime import date, datetime

from app.base_entity import BaseEntity


class ChildIn(BaseEntity):
    child_id: str


class PeriodOut(BaseEntity):
    id: int
    start_date: date
    end_date: date | None
    comment: str


class TeacherOut(BaseEntity):
    id: int
    last_name: str
    first_name: str
    phone: str
    email: str


class SchoolOut(BaseEntity):
    id: int
    name: str


class ClassOut(BaseEntity):
    id: int
    number: int
    letter: str
    has_breakfast: bool
    has_lunch: bool
    has_dinner: bool
    teachers: list[TeacherOut]
    school: SchoolOut


class ChildOut(BaseEntity):
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


class PlanIn(BaseEntity):
    breakfast: bool | None = None
    lunch: bool | None = None
    dinner: bool | None = None


class PlanOut(BaseEntity):
    breakfast: bool
    lunch: bool
    dinner: bool
