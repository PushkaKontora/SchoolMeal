from dependency_injector.wiring import Provide, inject

from app.legacy.container import AppContainer
from app.legacy.db.unit_of_work import UnitOfWork
from app.legacy.portions.db.portion.filters import ByPortionId
from app.legacy.portions.db.portion.joins import WithFood
from app.legacy.portions.db.portion.model import Portion
from app.legacy.portions.domain.entities import PortionOut
from app.legacy.portions.domain.errors import NotFoundPortionError


@inject
async def get_portion_by_id(portion_id: int, uow: UnitOfWork = Provide[AppContainer.unit_of_work]) -> PortionOut:
    async with uow:
        portion = await uow.repository(Portion).find_first(ByPortionId(portion_id), WithFood())

        if portion is None:
            raise NotFoundPortionError

        return PortionOut.from_orm(portion) if portion is not None else None
