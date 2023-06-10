from datetime import date as datetype

from app.db.specifications import FilterSpecification, TQuery
from app.meals.db.meal.model import Meal
from app.school_classes.db.school_class.model import SchoolClass


class ById(FilterSpecification):
    def __init__(self, meal_id: int):
        self._meal_id = meal_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.id == self._meal_id)


class BySomeClassId(FilterSpecification):
    def __init__(self, class_id: int | None):
        self._class_id = class_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.class_id == self._class_id) if self._class_id is not None else query


class BySomeDateFromInclusive(FilterSpecification):
    def __init__(self, date_from: datetype | None):
        self._date_from = date_from

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.date >= self._date_from) if self._date_from is not None else query


class BySomeDateToInclusive(FilterSpecification):
    def __init__(self, date_to: datetype | None):
        self._date_to = date_to

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.date <= self._date_to) if self._date_to is not None else query


class BySomeSchoolId(FilterSpecification):
    def __init__(self, school_id: int | None):
        self._school_id = school_id

    def __call__(self, query: TQuery) -> TQuery:
        return (
            query.join(SchoolClass).where(SchoolClass.school_id == self._school_id)
            if self._school_id is not None
            else query
        )


class BySomeDate(FilterSpecification):
    def __init__(self, date: datetype):
        self._date = date

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.date == self._date) if self._date is not None else query
