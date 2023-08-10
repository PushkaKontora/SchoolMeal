from sqlalchemy.orm import joinedload, selectinload

from app.legacy.db.specifications import Specification, TQuery
from app.legacy.meal_requests.db.meal_request.model import MealRequest
from app.legacy.meals.db.meal.model import Meal
from app.legacy.meals.db.menu.model import Menu
from app.legacy.portions.db.portion.model import Portion


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


class WithRequest(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Meal.request))


class WithDeclaredPupils(Specification):
    def __call__(self, query: TQuery) -> TQuery:
        return query.options(joinedload(Meal.request).selectinload(MealRequest.declared_pupils))
