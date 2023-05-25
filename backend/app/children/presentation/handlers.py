from fastapi import Body, Depends, Path

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.dependencies import JWTAuth
from app.children.domain.entities import ChildIn, ChildOut, PlanIn, PlanOut
from app.children.domain.services import (
    add_pupil_to_parent_children,
    change_meal_plan_by_parent,
    get_child_by_id,
    get_parent_children,
)
from app.utils.responses import SuccessResponse


async def add_child(schema: ChildIn = Body(), payload: JWTPayload = Depends(JWTAuth())) -> SuccessResponse:
    await add_pupil_to_parent_children(payload.user_id, schema)

    return SuccessResponse()


async def get_children(payload: JWTPayload = Depends(JWTAuth())) -> list[ChildOut]:
    return await get_parent_children(payload.user_id)


async def change_meal_plan(
    child_id: str = Path(), plan: PlanIn = Body(), payload: JWTPayload = Depends(JWTAuth())
) -> PlanOut:
    return await change_meal_plan_by_parent(payload.user_id, child_id, plan)


async def get_child(child_id: str = Path(), payload: JWTPayload = Depends(JWTAuth())) -> ChildOut:
    return await get_child_by_id(payload.user_id, child_id)
