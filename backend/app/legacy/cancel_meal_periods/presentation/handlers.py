from fastapi import Body, Depends, Path

from app.legacy.auth.domain.entities import JWTPayload
from app.legacy.auth.presentation.dependencies import JWTAuth
from app.legacy.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.legacy.cancel_meal_periods.domain.services import create_period_by_parent, delete_period_by_parent
from app.legacy.utils.responses import SuccessResponse


async def create_period(period: PeriodIn = Body(), payload: JWTPayload = Depends(JWTAuth())) -> PeriodOut:
    return await create_period_by_parent(payload.user_id, period)


async def delete_period(period_id: int = Path(), payload: JWTPayload = Depends(JWTAuth())) -> SuccessResponse:
    await delete_period_by_parent(payload.user_id, period_id)

    return SuccessResponse()
