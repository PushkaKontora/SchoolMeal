from datetime import date

import pytest
from httpx import AsyncClient, Response
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cancel_meal_periods.db.cancel_meal_period.model import CancelMealPeriod
from app.children.db.child.model import Child
from app.config import JWTSettings
from app.pupils.db.pupil.model import Pupil
from app.users.db.user.model import User
from tests.auth.integration.conftest import create_access_token
from tests.cancel_meal_periods.integration.conftest import period_prefix
from tests.conftest import BearerAuth
from tests.responses import SUCCESS, error


async def delete_period(client: AsyncClient, jwt_settings: JWTSettings, parent: User, period_id: int) -> Response:
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.delete(period_prefix(period_id), auth=BearerAuth(token))


async def test_deleting(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    period: CancelMealPeriod,
):
    response = await delete_period(client, jwt_settings, parent, period.id)

    assert response.status_code == 200
    assert response.json() == SUCCESS

    assert (
        await session.scalar(
            select(CancelMealPeriod).with_only_columns(func.count()).where(CancelMealPeriod.pupil_id == pupil.id)
        )
        == 1
    )
    assert (
        await session.execute(select(CancelMealPeriod).where(CancelMealPeriod.id == period.id))
    ).scalar_one_or_none() is None


async def test_deleting_by_not_parent_of_the_child(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    period: CancelMealPeriod,
):
    await session.execute(delete(Child).where(Child.parent_id == parent.id, Child.pupil_id == pupil.id))
    await session.commit()

    response = await delete_period(client, jwt_settings, parent, period.id)

    assert response.status_code == 403
    assert response.json() == error("UserIsNotParentError", "The user is not a parent of the pupil")

    assert (
        await session.scalar(
            select(CancelMealPeriod).with_only_columns(func.count()).where(CancelMealPeriod.pupil_id == pupil.id)
        )
        == 2
    )


async def test_deleting_unknown_period(
    client: AsyncClient, session: AsyncSession, jwt_settings: JWTSettings, parent: User, period: CancelMealPeriod
):
    response = await delete_period(client, jwt_settings, parent, 0)

    assert response.status_code == 404
    assert response.json() == error("NotFoundPeriodError", "Not found period")

    pupil_ids = select(Child).with_only_columns(Child.pupil_id).where(Child.parent_id == parent.id).scalar_subquery()
    query = select(CancelMealPeriod).with_only_columns(func.count()).where(CancelMealPeriod.pupil_id == pupil_ids)
    assert await session.scalar(query) == 2


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, pupil: Pupil):
    session.add(Child(parent_id=parent.id, pupil_id=pupil.id))
    session.add(CancelMealPeriod(pupil_id=pupil.id, start_date=date.fromisoformat("2011-07-10")))
    await session.commit()
