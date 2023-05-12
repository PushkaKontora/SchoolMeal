from fastapi import APIRouter

from app.users.presentation.handlers import get_profile, register_parent
from app.utils.responses import ErrorResponse


def get_users_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=register_parent,
        status_code=201,
        responses={400: {"model": ErrorResponse}},
    )

    router.include_router(get_me_router(), prefix="/me")

    return router


def get_me_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=get_profile,
        responses={404: {"model": ErrorResponse}},
    )

    return router
