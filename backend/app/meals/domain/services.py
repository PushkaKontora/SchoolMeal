from typing import Iterable

from dependency_injector.wiring import Provide, inject

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.meals.db.meal.filters import BySomeClassId, BySomeDateFromInclusive, BySomeDateToInclusive
from app.meals.db.meal.joins import WithFoods, WithMenus, WithPortions, WithSchoolClass
from app.meals.db.meal.model import Meal
from app.meals.db.menu.model import MealType, Menu
from app.meals.domain.entities import MealOut, MealsOptions, MealTypeOut, MenuOut
from app.portions.db.portion.model import Portion
from app.portions.domain.entities import PortionOut
from app.school_classes.db.school_class.model import SchoolClass


@inject
async def get_meals_by_filters(
    options: MealsOptions, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> list[MealOut]:
    async with uow:
        spec = (
            BySomeClassId(options.class_id)
            & BySomeDateFromInclusive(options.date_from)
            & BySomeDateToInclusive(options.date_to)
        )

        meals = await uow.repository(Meal).find(spec, WithSchoolClass(), WithMenus(), WithPortions(), WithFoods())

    return [_get_meal_out(meal) for meal in meals]


def _get_meal_out(meal: Meal) -> MealOut:
    menus: list[Menu] = meal.menus
    school_class: SchoolClass = meal.school_class

    portions: dict[MealType, list[Portion]] = {k: [] for k in MealType}

    for menu in menus:
        portions[menu.meal_type].append(menu.portion)

    return MealOut(
        id=meal.id,
        class_id=meal.class_id,
        date=meal.date,
        menu=MenuOut(
            breakfast=_get_meal_type_out(portions[MealType.BREAKFAST]) if school_class.has_breakfast else None,
            lunch=_get_meal_type_out(portions[MealType.LUNCH]) if school_class.has_lunch else None,
            dinner=_get_meal_type_out(portions[MealType.DINNER]) if school_class.has_dinner else None,
        ),
    )


def _get_meal_type_out(portions: Iterable[Portion]) -> MealTypeOut:
    portions_out = [PortionOut.from_orm(portion) for portion in portions]
    price = sum(portion.price for portion in portions)

    return MealTypeOut(price=price, portions=portions_out)
