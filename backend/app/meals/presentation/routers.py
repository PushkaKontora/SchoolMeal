from fastapi import APIRouter

from app.meals.presentation.handlers import MealsHandlers


class MealsRouter(APIRouter):
    def __init__(self, meals_handlers: MealsHandlers):
        super().__init__(tags=["meals"], prefix="/meals")

        self.add_api_route(
            path="",
            methods=["GET"],
            endpoint=meals_handlers.get_meals,
        )
