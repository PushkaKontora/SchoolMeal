from dependency_injector.wiring import Provide, inject

from app.cancel_meal_periods.db.cancel_meal_period.filters import ByPeriodId
from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.cancel_meal_periods.domain.entities import PeriodIn, PeriodOut
from app.cancel_meal_periods.domain.errors import NotFoundPeriodError, UserIsNotParentError
from app.children.db.child.filters import ByParentId, ByPupilId
from app.children.db.child.model import Child
from app.container import Container
from app.db.unit_of_work import UnitOfWork


@inject
async def create_period_by_parent(
    parent_id: int, period_in: PeriodIn, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> PeriodOut:
    async with uow:
        if not await uow.repository(Child).exists(ByParentId(parent_id) & ByPupilId(period_in.pupil_id)):
            raise UserIsNotParentError

        period = CancelMealPeriod(
            pupil_id=period_in.pupil_id,
            start_date=period_in.start_date,
            end_date=period_in.end_date,
            comment=period_in.comment,
        )
        uow.repository(CancelMealPeriod).save(period)
        await uow.commit()

        return PeriodOut(
            pupil_id=period_in.pupil_id,
            start_date=period_in.start_date,
            end_date=period_in.end_date,
            comment=period_in.comment,
        )


@inject
async def delete_period_by_parent(
    parent_id: int, period_id: int, uow: UnitOfWork = Provide[Container.unit_of_work]
) -> None:
    async with uow:
        period = await uow.repository(CancelMealPeriod).find_first(ByPeriodId(period_id))
        if not period:
            raise NotFoundPeriodError

        if not await uow.repository(Child).exists(ByParentId(parent_id) & ByPupilId(period.pupil_id)):
            raise UserIsNotParentError

        await uow.repository(CancelMealPeriod).delete(period)
        await uow.commit()
