from fastapi import APIRouter

from app.auth.presentation.handlers import logout, refresh_tokens, signin
from app.responses import ErrorResponse


def get_auth_router() -> APIRouter:
    router = APIRouter()

    router.add_api_route(path="/signin", methods=["POST"], endpoint=signin, responses={401: {"model": ErrorResponse}})

    router.add_api_route(
        path="/logout",
        methods=["POST"],
        endpoint=logout,
        responses={400: {"model": ErrorResponse}},
    )

    router.add_api_route(
        path="/refresh-tokens",
        methods=["POST"],
        endpoint=refresh_tokens,
        responses={400: {"model": ErrorResponse}},
    )

    return router
