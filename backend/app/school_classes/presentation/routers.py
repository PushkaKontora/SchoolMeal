from fastapi import APIRouter, Depends

from app.auth.presentation.dependencies import NotParentAuth
from app.school_classes.presentation.handlers import get_school_classes
from app.utils.responses import ErrorResponse


def get_school_classes_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(
        path="",
        endpoint=get_school_classes,
        responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}},
        dependencies=[Depends(NotParentAuth())],
    )

    return router
