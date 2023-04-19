from fastapi import APIRouter

from app.exceptions import ErrorResponse
from app.users.presentation.handlers import UsersHandlers


class UsersRouter(APIRouter):
    def __init__(self, users_handlers: UsersHandlers):
        super().__init__(tags=["users"], prefix="/users")

        self.add_api_route(
            path="",
            methods=["POST"],
            endpoint=users_handlers.register_parent,
            status_code=201,
            responses={400: {"model": ErrorResponse}},
        )
