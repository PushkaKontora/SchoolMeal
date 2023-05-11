from fastapi import Depends

from app.meals.domain.entities import MealOut, MealsOptions
from app.meals.domain.services import get_meals_by_filters


async def get_meals(params: MealsOptions = Depends()) -> list[MealOut]:
    return await get_meals_by_filters(params)
