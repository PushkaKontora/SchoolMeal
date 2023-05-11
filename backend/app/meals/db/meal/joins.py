from sqlalchemy.orm import joinedload, selectinload

from app.database.specifications import Specification, TQuery
from app.meals.db.meal.model import Meal
from app.meals.db.menu.model import Menu
from app.portions.db.portion.model import Portion


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
