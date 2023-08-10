from fastapi import APIRouter

from app.legacy.portions.presentation.handlers import get_portion
from app.legacy.utils.responses import ErrorResponse


def get_portions_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="/{portion_id:int}",
        methods=["GET"],
        endpoint=get_portion,
        responses={404: {"model": ErrorResponse}},
    )

    return router
