from fastapi import Body, Depends, Path

from app.legacy.auth.domain.entities import JWTPayload
from app.legacy.auth.presentation.dependencies import NotParentAuth
from app.legacy.meal_requests.domain.entities import (
    ExtendedMealRequestOut,
    MealRequestIn,
    MealRequestOut,
    MealRequestPutIn,
    MealRequestsGetOptions,
)
from app.legacy.meal_requests.domain.services import create_request_by_user, get_requests_by_options, update_request


async def get_requests(options: MealRequestsGetOptions = Depends()) -> list[ExtendedMealRequestOut]:
    return await get_requests_by_options(options)


async def create_request(
    payload: JWTPayload = Depends(NotParentAuth()), data: MealRequestIn = Body()
) -> MealRequestOut:
    return await create_request_by_user(payload.user_id, data)


async def update_pupils_in_request(request_id: int = Path(), data: MealRequestPutIn = Body()) -> MealRequestOut:
    return await update_request(request_id, data)
