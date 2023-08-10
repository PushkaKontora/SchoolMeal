from fastapi import Body, Depends, Path

from app.legacy.auth.domain.entities import JWTPayload
from app.legacy.auth.presentation.dependencies import JWTAuth
from app.legacy.children.domain.entities import ChildIn, PlanIn, PlanOut
from app.legacy.children.domain.services import (
    add_pupil_to_children,
    change_meal_plan_by_parent_id,
    get_child_by_id,
    get_children_by_parent_id,
)
from app.legacy.pupils.domain.entities import PupilWithClassAndPeriodsOut
from app.legacy.utils.responses import SuccessResponse


async def add_child(schema: ChildIn = Body(), payload: JWTPayload = Depends(JWTAuth())) -> SuccessResponse:
    await add_pupil_to_children(payload.user_id, schema)

    return SuccessResponse()


async def get_children(payload: JWTPayload = Depends(JWTAuth())) -> list[PupilWithClassAndPeriodsOut]:
    return await get_children_by_parent_id(payload.user_id)


async def change_meal_plan(
    child_id: str = Path(), plan: PlanIn = Body(), payload: JWTPayload = Depends(JWTAuth())
) -> PlanOut:
    return await change_meal_plan_by_parent_id(payload.user_id, child_id, plan)


async def get_child(child_id: str = Path(), payload: JWTPayload = Depends(JWTAuth())) -> PupilWithClassAndPeriodsOut:
    return await get_child_by_id(payload.user_id, child_id)
