from datetime import date, datetime

from app.base_entity import BaseEntity


class NewChildSchema(BaseEntity):
    child_id: str


class CancelMealPeriodOut(BaseEntity):
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


class ClassOut(BaseEntity):
    id: int
    number: int
    letter: str
    has_breakfast: bool
    has_lunch: bool
    has_dinner: bool
    teachers: list[TeacherOut]


class SchoolOut(BaseEntity):
    id: int
    name: str


class ChildOut(BaseEntity):
    id: str
    last_name: str
    first_name: str
    certificate_before_date: datetime | None
    balance: float
    breakfast: bool
    lunch: bool
    dinner: bool
    school_class: ClassOut
    school: SchoolOut
    cancel_meal_periods: list[CancelMealPeriodOut]


class MealPlanIn(BaseEntity):
    breakfast: bool | None = None
    lunch: bool | None = None
    dinner: bool | None = None


class MealPlanOut(BaseEntity):
    breakfast: bool
    lunch: bool
    dinner: bool
