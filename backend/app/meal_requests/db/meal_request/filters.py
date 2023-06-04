from app.db.specifications import FilterSpecification, TQuery
from app.meal_requests.db.meal_request.model import MealRequest


class ByMealId(FilterSpecification):
    def __init__(self, meal_id: int):
        self._meal_id = meal_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(MealRequest.meal_id == self._meal_id)


class ById(FilterSpecification):
    def __init__(self, request_id: int):
        self._request_id = request_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(MealRequest.id == self._request_id)
