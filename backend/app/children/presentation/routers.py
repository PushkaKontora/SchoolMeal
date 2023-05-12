from fastapi import APIRouter

from app.children.presentation.handlers import add_child, change_meal_plan, get_children
from app.utils.responses import ErrorResponse


def get_children_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        methods=["POST"],
        endpoint=add_child,
        responses={400: {"model": ErrorResponse}},
    )

    router.add_api_route(
        path="",
        methods=["GET"],
        endpoint=get_children,
    )

    router.include_router(get_child_router(), prefix="/{child_id:str}")

    return router


def get_child_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(path="", methods=["PATCH"], endpoint=change_meal_plan)

    return router
