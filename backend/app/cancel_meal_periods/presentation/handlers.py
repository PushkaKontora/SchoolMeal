from fastapi import Body, Depends, Path

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.middlewares import JWTAuth
from app.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.cancel_meal_periods.domain.services import create_period_by_parent, delete_period_by_parent
from app.utils.responses import SuccessResponse


async def create_period(period: PeriodIn = Body(), payload: JWTPayload = Depends(JWTAuth())) -> PeriodOut:
    return await create_period_by_parent(payload.user_id, period)


async def delete_period(period_id: int = Path(), payload: JWTPayload = Depends(JWTAuth())) -> SuccessResponse:
    await delete_period_by_parent(payload.user_id, period_id)

    return SuccessResponse()
