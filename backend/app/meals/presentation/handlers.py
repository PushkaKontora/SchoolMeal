from fastapi import Depends

from app.meals.domain.entities import MealOut, MealsOptions
from app.meals.domain.services import MealService


class MealsHandlers:
    def __init__(self, meal_service: MealService):
        self._meal_service = meal_service

    async def get_meals(self, params: MealsOptions = Depends()) -> list[MealOut]:
        return await self._meal_service.get_meals(params)
