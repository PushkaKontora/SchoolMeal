from datetime import date

from app.db.specifications import FilterSpecification, TQuery
from app.meals.db.meal.model import Meal


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
    def __init__(self, date_from: date | None):
        self._date_from = date_from

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.date >= self._date_from) if self._date_from is not None else query


class BySomeDateToInclusive(FilterSpecification):
    def __init__(self, date_to: date | None):
        self._date_to = date_to

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(Meal.date <= self._date_to) if self._date_to is not None else query
