from dependency_injector.wiring import Provide, inject

from app.appcontainer import AppContainer
from app.db.unit_of_work import UnitOfWork
from app.portions.db.portion.filters import ByPortionId
from app.portions.db.portion.joins import WithFood
from app.portions.db.portion.model import Portion
from app.portions.domain.entities import PortionOut
from app.portions.domain.errors import NotFoundPortionError


@inject
async def get_portion_by_id(portion_id: int, uow: UnitOfWork = Provide[AppContainer.unit_of_work]) -> PortionOut:
    async with uow:
        portion = await uow.repository(Portion).find_first(ByPortionId(portion_id), WithFood())

        if portion is None:
            raise NotFoundPortionError

        return PortionOut.from_orm(portion) if portion is not None else None
