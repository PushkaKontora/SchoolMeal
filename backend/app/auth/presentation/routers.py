from fastapi import APIRouter

from app.auth.presentation.handlers import AuthHandlers
from app.exceptions import ErrorResponse


class AuthRouter(APIRouter):
    def __init__(self, auth_handlers: AuthHandlers):
        super().__init__(tags=["auth"], prefix="/auth")

        self.add_api_route(
            path="/signin", methods=["POST"], endpoint=auth_handlers.signin, responses={401: {"model": ErrorResponse}}
        )

        self.add_api_route(
            path="/logout",
            methods=["POST"],
            endpoint=auth_handlers.logout,
        )

        self.add_api_route(
            path="/refresh-tokens",
            methods=["POST"],
            endpoint=auth_handlers.refresh_tokens,
        )
