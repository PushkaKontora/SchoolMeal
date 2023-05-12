from dependency_injector.wiring import Provide, inject

from app.container import Container
from app.db.unit_of_work import UnitOfWork
from app.portions.db.portion.filters import ByPortionId
from app.portions.db.portion.joins import WithFood
from app.portions.db.portion.model import Portion
from app.portions.domain.entities import PortionOut
from app.portions.domain.exceptions import NotFoundPortionException


@inject
async def get_portion_by_id(portion_id: int, uow: UnitOfWork = Provide[Container.unit_of_work]) -> PortionOut:
    async with uow:
        portion = await uow.repository(Portion).find_first(ByPortionId(portion_id), WithFood())

        if portion is None:
            raise NotFoundPortionException

        return PortionOut.from_orm(portion) if portion is not None else None
