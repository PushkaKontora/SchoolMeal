from fastapi import APIRouter

from app.cancel_meal_periods.presentation.handlers import create_period, delete_period
from app.utils.responses import ErrorResponse


def get_cancel_meal_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=create_period,
        responses={400: {"model": ErrorResponse}},
        status_code=201,
    )

    router.add_api_route(
        path="/{period_id:int}",
        methods=["DELETE"],
        endpoint=delete_period,
        responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
    )

    return router
