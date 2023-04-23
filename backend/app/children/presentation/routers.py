from fastapi import APIRouter, Depends

from app.auth.presentation.middlewares import JWTAuth
from app.children.presentation.handlers import ChildrenHandlers
from app.exceptions import ErrorResponse


class ChildrenRouter(APIRouter):
    def __init__(self, children_handlers: ChildrenHandlers, jwt_auth: JWTAuth):
        super().__init__(tags=["children"], prefix="/children")

        self.add_api_route(
            path="",
            methods=["POST"],
            endpoint=children_handlers.add_child,
            responses={400: {"model": ErrorResponse}},
            dependencies=[Depends(jwt_auth)],
        )
