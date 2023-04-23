from fastapi import Request

from app.base_entity import SuccessResponse
from app.children.domain.entities import NewChildSchema
from app.children.domain.services import ChildService


class ChildrenHandlers:
    def __init__(self, child_service: ChildService):
        self._child_service = child_service

    async def add_child(self, request: Request, schema: NewChildSchema) -> SuccessResponse:
        await self._child_service.add_child(request.payload.user_id, schema.child_id)

        return SuccessResponse()
