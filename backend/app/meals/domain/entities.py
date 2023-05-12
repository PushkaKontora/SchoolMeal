from datetime import date

from app.portions.domain.entities import PortionOut
from app.utils.entity import Entity


class MealsOptions(Entity):
    class_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None


class MealTypeOut(Entity):
    price: float
    portions: list[PortionOut]


class MenuOut(Entity):
    breakfast: MealTypeOut | None
    lunch: MealTypeOut | None
    dinner: MealTypeOut | None


class MealOut(Entity):
    id: int
    class_id: int
    date: date
    menu: MenuOut
