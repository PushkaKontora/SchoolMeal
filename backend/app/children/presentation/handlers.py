from fastapi import Body, Path, Request

from app.base_entity import SuccessResponse
from app.children.domain.entities import ChildOut, MealPlanIn, MealPlanOut, NewChildSchema
from app.children.domain.services import ChildService


class ChildrenHandlers:
    def __init__(self, child_service: ChildService):
        self._child_service = child_service

    async def add_child(self, request: Request, schema: NewChildSchema) -> SuccessResponse:
        await self._child_service.add_child(request.payload.user_id, schema.child_id)

        return SuccessResponse()

    async def get_children(self, request: Request) -> list[ChildOut]:
        return await self._child_service.get_children(request.payload.user_id)


class ChildHandlers:
    def __init__(self, child_service: ChildService):
        self._child_service = child_service

    async def change_meal_plan(
        self, request: Request, child_id: str = Path(...), plan: MealPlanIn = Body(...)
    ) -> MealPlanOut:
        return await self._child_service.change_meal_plan(request.payload.user_id, child_id, **plan.dict())
