from fastapi import APIRouter, Depends

from app.auth.presentation.dependencies import JWTAuth
from app.meal_requests.presentation.handlers import create_request, update_pupils_in_request
from app.utils.responses import ErrorResponse


def get_meal_requests_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=create_request,
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
    )

    router.add_api_route(
        path="/{request_id:int}",
        methods=["PUT"],
        endpoint=update_pupils_in_request,
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
        dependencies=[Depends(JWTAuth())],
    )

    return router
