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
from tests.integration.auth.conftest import create_access_token
from tests.integration.cancel_meal_periods.conftest import PERIODS_PREFIX
from tests.integration.conftest import BearerAuth
from tests.integration.responses import error


pytestmark = [pytest.mark.integration]

MAX_COMMENT_LENGTH = 512


async def create(
    client: AsyncClient,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    start_date: date,
    end_date: date | None,
    comment: str | None,
) -> Response:
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.post(
        url=PERIODS_PREFIX,
        json={
            "pupilId": pupil.id,
            "startDate": str(start_date),
            "endDate": str(end_date) if end_date else None,
            "comment": comment,
        },
        auth=BearerAuth(token),
    )


@pytest.mark.parametrize(
    ["start_date", "end_date", "comment", "status_code"],
    [
        ["2023-04-10", None, None, 201],
        ["2023-04-10", None, "some comment", 201],
        ["2023-04-10", "2023-04-11", None, 201],
        ["2023-04-10", "2023-04-11", "some comment", 201],
        ["2023-04-10", "2023-04-10", None, 422],
        ["2023-04-10", "2023-04-09", None, 422],
        ["2023-04-10", None, "a" * MAX_COMMENT_LENGTH, 201],
        ["2023-04-10", None, "a" * (MAX_COMMENT_LENGTH + 1), 422],
    ],
)
async def test_creating(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    start_date: str,
    end_date: str | None,
    comment: str | None,
    status_code: int,
):
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date) if end_date is not None else None

    response = await create(client, jwt_settings, parent, pupil, start, end, comment)

    assert response.status_code == status_code, response.text
    match status_code:
        case 201:
            assert response.json() == {
                "pupilId": pupil.id,
                "startDate": start_date,
                "endDate": end_date,
                "comment": comment,
            }

            query = select(CancelMealPeriod).where(CancelMealPeriod.pupil_id == pupil.id)
            actual: CancelMealPeriod = (await session.execute(query)).scalar_one()
            assert actual.start_date == start
            assert actual.end_date == end
            assert actual.comment == comment

        case 422:
            q = select(CancelMealPeriod).with_only_columns(func.count()).where(CancelMealPeriod.pupil_id == pupil.id)
            assert await session.scalar(q) == 0

        case _:
            raise Exception(f"Unhandled status code {status_code}")


async def test_creating_by_not_parent(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    start_date="2023-04-10",
):
    query = delete(Child).where(Child.parent_id == parent.id, Child.pupil_id == pupil.id)
    await session.execute(query)
    await session.commit()

    response = await create(client, jwt_settings, parent, pupil, date.fromisoformat(start_date), None, None)

    assert response.status_code == 403
    assert response.json() == error("UserIsNotParentError", "The user is not a parent of the pupil")

    q = select(CancelMealPeriod).with_only_columns(func.count()).where(CancelMealPeriod.pupil_id == pupil.id)
    assert await session.scalar(q) == 0


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, pupil: Pupil):
    session.add(Child(parent_id=parent.id, pupil_id=pupil.id))
    await session.commit()
