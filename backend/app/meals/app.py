from fastapi import FastAPI

from app.meals.presentation.routers import get_meals_router


def register_meals_api(app: FastAPI) -> None:
    app.include_router(
        router=get_meals_router(),
        prefix="/meals",
        tags=["meals"],
    )
