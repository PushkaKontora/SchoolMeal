from fastapi import APIRouter, Depends

from app.auth.presentation.dependencies import NotParentAuth
from app.school_classes.presentation.handlers import get_pupils, get_school_classes
from app.utils.responses import ErrorResponse


def get_school_classes_router() -> APIRouter:
    router = APIRouter(
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
        dependencies=[Depends(NotParentAuth())],
    )

    router.add_api_route(
        path="",
        endpoint=get_school_classes,
    )

    router.add_api_route(path="/{class_id:int}/pupils", endpoint=get_pupils)

    return router
