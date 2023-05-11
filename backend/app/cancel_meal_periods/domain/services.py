from dependency_injector.wiring import Provide, inject

from app.cancel_meal_periods.db.cancel_meal_period.filters import ByPeriodId
from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.cancel_meal_periods.domain.exceptions import NotFoundPeriodException, UserIsNotParentException
from app.children.db.parent_pupil.filters import ByParentId, ByPupilId
from app.database.container import Database
from app.database.unit_of_work import UnitOfWork


@inject
async def create_period_by_parent(
    parent_id: int, period_in: PeriodIn, uow: UnitOfWork = Provide[Database.unit_of_work]
) -> PeriodOut:
    async with uow:
        if not await uow.children_repo.exists(ByParentId(parent_id) & ByPupilId(period_in.pupil_id)):
            raise UserIsNotParentException

        period = CancelMealPeriod(
            pupil_id=period_in.pupil_id,
            start_date=period_in.start_date,
            end_date=period_in.end_date,
            comment=period_in.comment,
        )
        uow.cancel_meal_periods_repo.save(period)
        await uow.commit()

        return PeriodOut(
            pupil_id=period_in.pupil_id,
            start_date=period_in.start_date,
            end_date=period_in.end_date,
            comment=period_in.comment,
        )


@inject
async def delete_period_by_parent(
    parent_id: int, period_id: int, uow: UnitOfWork = Provide[Database.unit_of_work]
) -> None:
    async with uow:
        period = await uow.cancel_meal_periods_repo.find_one(ByPeriodId(period_id))
        if not period:
            raise NotFoundPeriodException

        if not await uow.children_repo.exists(ByParentId(parent_id) & ByPupilId(period.pupil_id)):
            raise UserIsNotParentException

        await uow.cancel_meal_periods_repo.delete(period)
        await uow.commit()
