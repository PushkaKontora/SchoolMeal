from sqlalchemy.orm import joinedload, selectinload

from app.database.specifications import Specification, TQuery
from app.foods.db.portion.model import Portion
from app.meals.db.meal.model import Meal
from app.meals.db.menu.model import Menu


class WithSchoolClass(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Meal.school_class))


class WithMenus(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(selectinload(Meal.menus))


class WithPortions(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(selectinload(Meal.menus).joinedload(Menu.portion))


class WithFoods(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(selectinload(Meal.menus).joinedload(Menu.portion).joinedload(Portion.food))
