from sqlalchemy.orm import joinedload, selectinload

from app.legacy.db.specifications import Specification, TQuery
from app.legacy.pupils.db.pupil.model import Pupil
from app.legacy.school_classes.db.school_class.model import SchoolClass


class WithClass(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Pupil.school_class))


class WithSchool(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Pupil.school_class).selectinload(SchoolClass.school))


class WithTeachers(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Pupil.school_class).selectinload(SchoolClass.teachers))


class WithCancelMealPeriods(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(selectinload(Pupil.cancel_meal_periods))
