from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.legacy.cancel_meal_periods import CancelMealPeriod
from app.legacy.pupils.db.pupil.model import Pupil


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
