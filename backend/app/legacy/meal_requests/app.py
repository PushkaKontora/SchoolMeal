from fastapi import FastAPI

from app.legacy.meal_requests.presentation.routers import get_meal_requests_router


def register_meal_requests_api(app: FastAPI) -> None:
    app.include_router(
        router=get_meal_requests_router(),
        prefix="/meal-requests",
        tags=["Meal Requests"],
    )
