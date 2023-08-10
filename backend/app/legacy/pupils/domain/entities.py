from datetime import datetime

from app.legacy.cancel_meal_periods.domain.entities import PeriodOut
from app.legacy.school_classes.domain.entities import ClassWithTeachersOut
from app.legacy.utils.entity import Entity


class PupilOut(Entity):
    id: str
    last_name: str
    first_name: str
    certificate_before_date: datetime | None
    balance: float
    breakfast: bool
    lunch: bool
    dinner: bool


class PupilWithClassAndPeriodsOut(PupilOut):
    school_class: ClassWithTeachersOut | None
    cancel_meal_periods: list[PeriodOut]
