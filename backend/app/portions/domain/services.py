from dependency_injector.wiring import Provide, inject

from app.database.container import Database
from app.database.unit_of_work import UnitOfWork
from app.portions.db.portion.filters import ByPortionId
from app.portions.db.portion.joins import WithFood
from app.portions.domain.entities import PortionOut
from app.portions.domain.exceptions import NotFoundPortionException


@inject
async def get_portion_by_id(portion_id: int, uow: UnitOfWork = Provide[Database.unit_of_work]) -> PortionOut:
    async with uow:
        portion = await uow.portions_repo.find_one(ByPortionId(portion_id), WithFood())

        if portion is None:
            raise NotFoundPortionException

        return PortionOut.from_orm(portion) if portion is not None else None
