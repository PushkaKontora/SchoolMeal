from fastapi import Body, Path, Request

from app.base_entity import SuccessResponse
from app.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.cancel_meal_periods.domain.services import PeriodService


class PeriodsHandlers:
    def __init__(self, period_service: PeriodService):
        self._period_service = period_service

    async def create_period(self, request: Request, data: PeriodIn = Body(...)) -> PeriodOut:
        return await self._period_service.create_period(request.payload.user_id, data)

    async def delete_period(self, request: Request, period_id: int = Path(...)) -> SuccessResponse:
        await self._period_service.delete_period(request.payload.user_id, period_id)

        return SuccessResponse()
