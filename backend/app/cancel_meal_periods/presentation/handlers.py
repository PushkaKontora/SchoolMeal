from fastapi import Body, Request

from app.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.cancel_meal_periods.domain.services import PeriodService


class PeriodsHandlers:
    def __init__(self, period_service: PeriodService):
        self._period_service = period_service

    async def create_period(self, request: Request, data: PeriodIn = Body(...)) -> PeriodOut:
        return await self._period_service.create_period(request.payload.user_id, data)
