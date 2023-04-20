from fastapi import APIRouter, Depends

from app.auth.presentation.middlewares import JWTAuth
from app.exceptions import ErrorResponse
from app.users.presentation.handlers import MeHandlers, UsersHandlers


class UsersRouter(APIRouter):
    def __init__(self, users_handlers: UsersHandlers, me_router: "MeRouter"):
        super().__init__(tags=["users"], prefix="/users")

        self.add_api_route(
            path="",
            methods=["POST"],
            endpoint=users_handlers.register_parent,
            status_code=201,
            responses={400: {"model": ErrorResponse}},
        )

        self.include_router(me_router)


class MeRouter(APIRouter):
    def __init__(self, me_handlers: MeHandlers, jwt_auth: JWTAuth):
        super().__init__(tags=["users"], prefix="/me")

        self.add_api_route(
            path="",
            methods=["GET"],
            endpoint=me_handlers.get_user_profile_by_token,
            responses={404: {"model": ErrorResponse}},
            dependencies=[Depends(jwt_auth)],
        )
