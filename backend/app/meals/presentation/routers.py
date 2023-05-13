from fastapi import APIRouter

from app.meals.presentation.handlers import get_meals


def get_meals_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=get_meals,
    )

    return router
