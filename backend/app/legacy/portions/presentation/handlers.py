from fastapi import Path

from app.legacy.portions.domain.entities import PortionOut
from app.legacy.portions.domain.services import get_portion_by_id


async def get_portion(portion_id: int = Path()) -> PortionOut:
    return await get_portion_by_id(portion_id)
