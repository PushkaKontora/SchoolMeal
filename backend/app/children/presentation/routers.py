from fastapi import APIRouter, Depends

from app.auth.presentation.middlewares import JWTAuth
from app.children.presentation.handlers import ChildHandlers, ChildrenHandlers
from app.exceptions import ErrorResponse


class ChildrenRouter(APIRouter):
    def __init__(self, children_handlers: ChildrenHandlers, child_router: "ChildRouter", jwt_auth: JWTAuth):
        super().__init__(tags=["children"], prefix="/children", dependencies=[Depends(jwt_auth)])

        self.add_api_route(
            path="",
            methods=["POST"],
            endpoint=children_handlers.add_child,
            responses={400: {"model": ErrorResponse}},
        )

        self.add_api_route(
            path="",
            methods=["GET"],
            endpoint=children_handlers.get_children,
        )

        self.include_router(child_router)


class ChildRouter(APIRouter):
    def __init__(self, child_handlers: ChildHandlers):
        super().__init__(prefix="/{child_id:str}")

        self.add_api_route(path="", methods=["PATCH"], endpoint=child_handlers.change_meal_plan)
