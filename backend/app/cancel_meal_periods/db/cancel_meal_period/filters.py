from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.database.specifications import FilterSpecification, TQuery


class ByPeriodId(FilterSpecification):
    def __init__(self, period_id: int):
        self._period_id = period_id

    def __call__(self, query: TQuery) -> TQuery:
        return query.where(CancelMealPeriod.id == self._period_id)
