from sqlalchemy.orm import joinedload

from app.db.specifications import FilterSpecification, TQuery
from app.meal_requests.db.meal_request.model import MealRequest
from app.meals.db.meal.model import Meal
from app.school_classes.db.school_class.model import SchoolClass
from app.schools.db.school.model import School


class _ByMealId(FilterSpecification):
    def __init__(self, meal_id: int):
        self._meal_id = meal_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(MealRequest.meal_id == self._meal_id)


class _ById(FilterSpecification):
    def __init__(self, request_id: int):
        self._request_id = request_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(MealRequest.id == self._request_id)


class _ByOptionSchoolId(FilterSpecification):
    def __init__(self, school_id: int | None):
        self._school_id = school_id

    def __call__(self, query: TQuery) -> TQuery:
        return (
            query.options(joinedload(MealRequest.meal).joinedload(Meal.school)).where(School.id == self._school_id)
            if self._school_id is not None
            else query
        )


class MealRequestFilters:
    ById = _ById
    ByMealId = _ByMealId
    ByOptionSchoolId = _ByOptionSchoolId
