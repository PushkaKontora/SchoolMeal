from fastapi import Body, Depends, Path

from app.auth.domain.entities import JWTPayload
from app.auth.presentation.middlewares import JWTAuth
from app.children.domain.entities import ChildIn, ChildOut, PlanIn, PlanOut
from app.children.domain.services import add_pupil_to_parent_children, change_meal_plan_by_parent, get_parent_children
from app.responses import SuccessResponse


async def add_child(schema: ChildIn = Body(), payload: JWTPayload = Depends(JWTAuth())) -> SuccessResponse:
    await add_pupil_to_parent_children(payload.user_id, schema)

    return SuccessResponse()


async def get_children(payload: JWTPayload = Depends(JWTAuth())) -> list[ChildOut]:
    return await get_parent_children(payload.user_id)


async def change_meal_plan(
    child_id: str = Path(), plan: PlanIn = Body(), payload: JWTPayload = Depends(JWTAuth())
) -> PlanOut:
    return await change_meal_plan_by_parent(payload.user_id, child_id, plan)
