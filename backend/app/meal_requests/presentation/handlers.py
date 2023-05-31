from fastapi import Body, Depends, Path

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.dependencies import NotParentAuth
from app.meal_requests.domain.entities import MealRequestIn, MealRequestOut, MealRequestPutIn
from app.meal_requests.domain.services import create_request_by_user, update_request


async def create_request(
    payload: JWTPayload = Depends(NotParentAuth()), data: MealRequestIn = Body()
) -> MealRequestOut:
    return await create_request_by_user(payload.user_id, data)


async def update_pupils_in_request(request_id: int = Path(), data: MealRequestPutIn = Body()) -> MealRequestOut:
    return await update_request(request_id, data)
