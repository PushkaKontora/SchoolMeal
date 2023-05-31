from datetime import datetime

from app.cancel_meal_periods.domain.entities import PeriodOut
from app.school_classes.domain.entities import ClassWithTeachersOut
from app.utils.entity import Entity


class PupilOut(Entity):
    id: str
    last_name: str
    first_name: str
    certificate_before_date: datetime | None
    balance: float
    breakfast: bool
    lunch: bool
    dinner: bool
    school_class: ClassWithTeachersOut | None
    cancel_meal_periods: list[PeriodOut]
