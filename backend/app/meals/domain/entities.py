from datetime import date

from app.base_entity import BaseEntity
from app.portions.domain.entities import PortionOut


class MealsOptions(BaseEntity):
    class_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None


class MealTypeOut(BaseEntity):
    price: float
    portions: list[PortionOut]


class MenuOut(BaseEntity):
    breakfast: MealTypeOut | None
    lunch: MealTypeOut | None
    dinner: MealTypeOut | None


class MealOut(BaseEntity):
    id: int
    class_id: int
    date: date
    menu: MenuOut
