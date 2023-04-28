from fastapi import APIRouter, Depends

from app.auth.presentation.middlewares import JWTAuth
from app.cancel_meal_periods.presentation.handlers import PeriodsHandlers
from app.exceptions import ErrorResponse


class CancelMealPeriodsRouter(APIRouter):
    def __init__(self, periods_handlers: PeriodsHandlers, jwt_auth: JWTAuth):
        super().__init__(tags=["cancel meal periods"], prefix="/cancel-meal-periods", dependencies=[Depends(jwt_auth)])

        self.add_api_route(
            path="",
            methods=["POST"],
            endpoint=periods_handlers.create_period,
            responses={400: {"model": ErrorResponse}},
            status_code=201,
        )

        self.add_api_route(
            path="/{period_id:int}",
            methods=["DELETE"],
            endpoint=periods_handlers.delete_period,
            responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
        )
