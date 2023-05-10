from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from app.meals.domain.services import MealService
from app.meals.presentation.handlers import MealsHandlers
from app.meals.presentation.routers import MealsRouter


class MealsAPI(DeclarativeContainer):
    meal_service = Factory(MealService)

    meals_handlers = Factory(MealsHandlers, meal_service=meal_service)

    router = Factory(MealsRouter, meals_handlers=meals_handlers)
