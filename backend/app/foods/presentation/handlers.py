from app.foods.domain.entities import PortionOut
from app.foods.domain.services import PortionService


class PortionsHandlers:
    def __init__(self, portion_service: PortionService):
        self._portion_service = portion_service

    async def get_portion(self, portion_id: int) -> PortionOut:
        return await self._portion_service.get_portion_by_id(portion_id)
