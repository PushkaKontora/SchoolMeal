from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.children.db.parent_pupil.model import ParentPupil
from app.pupils.db.pupil.model import Pupil
from app.users.db.user.model import User


PERIODS_PREFIX = "/cancel-meal-periods"


def period_prefix(period_id: int) -> str:
    return PERIODS_PREFIX + f"/{period_id}"


@pytest.fixture
async def period(session: AsyncSession, pupil: Pupil) -> CancelMealPeriod:
    period = CancelMealPeriod(
        pupil_id=pupil.id,
        start_date=date.fromisoformat("2023-04-28"),
    )
    session.add(period)
    await session.commit()
    await session.refresh(period)

    return period
