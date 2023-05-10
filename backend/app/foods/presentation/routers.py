from fastapi import APIRouter

from app.exceptions import ErrorResponse
from app.foods.presentation.handlers import PortionsHandlers


class PortionsRouter(APIRouter):
    def __init__(self, portions_handlers: PortionsHandlers):
        super().__init__(tags=["portions"], prefix="/portions")

        self.add_api_route(
            path="/{portion_id:int}",
            methods=["GET"],
            endpoint=portions_handlers.get_portion,
            responses={404: {"model": ErrorResponse}},
        )
