from abc import ABC

from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.database.base import Repository


class BaseCancelMealPeriodsRepository(Repository[CancelMealPeriod], ABC):
    pass
