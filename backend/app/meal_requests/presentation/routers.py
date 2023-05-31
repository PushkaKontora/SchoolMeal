from fastapi import APIRouter

from app.meal_requests.presentation.handlers import create_request
from app.utils.responses import ErrorResponse


def get_meal_requests_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=create_request,
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
    )

    return router
