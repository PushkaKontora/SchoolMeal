from fastapi import Body, Depends

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.dependencies import NotParentAuth
from app.meal_requests.domain.entities import MealRequestIn, MealRequestOut
from app.meal_requests.domain.services import create_request_by_user


async def create_request(
    payload: JWTPayload = Depends(NotParentAuth()), data: MealRequestIn = Body()
) -> MealRequestOut:
    return await create_request_by_user(payload.user_id, data)
