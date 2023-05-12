from fastapi import FastAPI

from app.cancel_meal_periods.presentation.routers import get_cancel_meal_router


def register_cancel_meal_periods_api(app: FastAPI) -> None:
    app.include_router(
        router=get_cancel_meal_router(),
        prefix="/cancel-meal-periods",
        tags=["cancel-meal-periods"],
    )
