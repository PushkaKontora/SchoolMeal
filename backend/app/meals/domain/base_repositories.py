from abc import ABC

from app.database.base import Repository
from app.meals.db.meal.model import Meal


class BaseMealsRepository(Repository[Meal], ABC):
    pass
