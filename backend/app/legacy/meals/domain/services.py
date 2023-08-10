from typing import Iterable

from dependency_injector.wiring import Provide, inject

from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.meals.db.meal.filters import BySomeClassId, BySomeDateFromInclusive, BySomeDateToInclusive
from app.legacy.meals.db.meal.joins import WithFoods, WithMenus, WithPortions, WithSchoolClass
from app.legacy.meals.db.meal.model import Meal
from app.legacy.meals.db.menu.model import MealType, Menu
from app.legacy.meals.domain.entities import MealOut, MealsOptions, MealTypeOut, MenuOut
from app.legacy.portions.db.portion.model import Portion
from app.legacy.portions.domain.entities import FoodOut, PortionOut
from app.legacy.school_classes.db.school_class.model import SchoolClass
from app.legacy.utils.storages import Storage


@inject
async def get_meals_by_filters(
    options: MealsOptions, uow: UnitOfWork = Provide[AppContainer.unit_of_work]
) -> list[MealOut]:
    async with uow:
        spec = (
            BySomeClassId(options.class_id)
            & BySomeDateFromInclusive(options.date_from)
            & BySomeDateToInclusive(options.date_to)
        )

        meals = await uow.repository(Meal).find(spec, WithSchoolClass(), WithMenus(), WithPortions(), WithFoods())

    return [await _get_meal_out(meal) for meal in meals]


async def _get_meal_out(meal: Meal) -> MealOut:
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
            breakfast=await _get_meal_type_out(portions[MealType.BREAKFAST]) if school_class.has_breakfast else None,
            lunch=await _get_meal_type_out(portions[MealType.LUNCH]) if school_class.has_lunch else None,
            dinner=await _get_meal_type_out(portions[MealType.DINNER]) if school_class.has_dinner else None,
        ),
    )


async def _get_meal_type_out(
    portions: Iterable[Portion], storage: Storage = Provide[AppContainer.storage]
) -> MealTypeOut:
    portions_out = [
        PortionOut(
            id=portion.id,
            price=portion.price,
            components=portion.components,
            weight=portion.weight,
            kcal=portion.kcal,
            protein=portion.protein,
            fats=portion.fats,
            carbs=portion.carbs,
            food=FoodOut(
                id=portion.food.id,
                school_id=portion.food.school_id,
                name=portion.food.name,
                photo_path=await storage.generate_url(portion.food.photo_path)
                if portion.food.photo_path is not None
                else None,
            ),
        )
        for portion in portions
    ]
    price = sum(portion.price for portion in portions)

    return MealTypeOut(price=price, portions=portions_out)
