from datetime import date

from pydantic import Field

from app.nutrition.application.context import NutritionContext
from app.nutrition.application.queries.dto import FoodOut, MealtimeInfo, MenuOut
from app.nutrition.domain.menu import Food
from app.nutrition.domain.school_class import SchoolClassType
from app.shared.cqs.queries import IQueryExecutor, Query
from app.shared.domain.money import Money
from app.shared.objects_storage.abc import IObjectsStorage
from app.shared.unit_of_work.abc import IUnitOfWork


class GetMenuOnDateQuery(Query):
    school_class_number: int = Field(ge=1, le=11)
    on_date: date


class GetMenuOnDateQueryExecutor(IQueryExecutor[GetMenuOnDateQuery, MenuOut]):
    def __init__(self, unit_of_work: IUnitOfWork[NutritionContext], objects_storage: IObjectsStorage) -> None:
        self._unit_of_work = unit_of_work
        self._objects = objects_storage

    async def execute(self, query: GetMenuOnDateQuery) -> MenuOut:
        """
        :raise NotFoundMenu: не найдено меню
        """

        async with self._unit_of_work as context:
            menu = await context.menus.get_by_class_type_and_date(
                school_class_type=SchoolClassType.from_number(query.school_class_number),
                on_date=query.on_date,
            )

            return MenuOut(
                id=menu.id,
                on_date=menu.on_date,
                breakfast=await self._get_mealtime_info(menu.breakfast_foods),
                dinner=await self._get_mealtime_info(menu.dinner_foods),
                snacks=await self._get_mealtime_info(menu.snacks_foods),
            )

    async def _get_mealtime_info(self, foods: list[Food]) -> MealtimeInfo:
        return MealtimeInfo(
            foods=[
                FoodOut(
                    id=food.id,
                    name=food.name,
                    description=food.description,
                    calories=str(food.calories),
                    proteins=str(food.proteins),
                    fats=str(food.fats),
                    carbohydrates=str(food.carbohydrates),
                    weight=str(food.weight),
                    price=str(food.price),
                    photo_url=await self._objects.get_url(file=food.photo),
                )
                for food in foods
            ],
            cost=str(sum((food.price for food in foods), start=Money(0))),
        )
