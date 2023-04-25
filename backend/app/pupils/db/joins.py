from sqlalchemy.orm import joinedload, selectinload

from app.database.specifications import Specification, TQuery
from app.pupils.db.models import Pupil
from app.school_classes.db.models import SchoolClass


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
