import pytest
from httpx import AsyncClient, Response
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.children.db.parent_pupil.model import ParentPupil
from app.config import JWTSettings
from app.pupils.db.pupil.model import Pupil
from app.users.db.user.model import User
from tests.auth.integration.conftest import create_access_token
from tests.children.integration.conftest import child_prefix
from tests.conftest import BearerAuth
from tests.responses import FORBIDDEN, error
from tests.utils import prepare_patch_data


pytestmark = [pytest.mark.integration]

MEALS = ("breakfast", "lunch", "dinner")


async def change(
    client: AsyncClient,
    jwt_settings: JWTSettings,
    parent: User,
    child: Pupil,
    breakfast: bool | None = None,
    lunch: bool | None = None,
    dinner: bool | None = None,
) -> Response:
    url = child_prefix(child.id)
    body = prepare_patch_data({"breakfast": breakfast, "lunch": lunch, "dinner": dinner})
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.patch(url, json=body, auth=BearerAuth(token))


@pytest.mark.parametrize(
    "plan",
    [
        {},
        {"breakfast": True},
        {"lunch": True},
        {"dinner": True},
        {"breakfast": True, "lunch": True, "dinner": True},
        {"breakfast": False, "lunch": False, "dinner": False},
    ],
    ids=[
        "empty body",
        "only breakfast",
        "only lunch",
        "only dinner",
        "all true",
        "all false",
    ],
)
async def test_change_meal_plan(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    child: Pupil,
    plan: dict,
):
    child.breakfast = child.lunch = child.dinner = False
    session.add(child)
    old_plan = {meal: getattr(child, meal) for meal in MEALS}
    await session.commit()

    response = await change(client, jwt_settings, parent, child, **plan)

    await session.refresh(child)

    assert response.status_code == 200
    assert response.json() == {
        "breakfast": child.breakfast,
        "lunch": child.lunch,
        "dinner": child.dinner,
    }

    actual = {meal: getattr(child, meal) for meal in MEALS}
    expected = {meal: plan.get(meal) or old_plan[meal] for meal in MEALS}
    assert actual == expected


async def test_change_the_childs_plan_by_some_parent(
    client: AsyncClient, session: AsyncSession, jwt_settings: JWTSettings, parent: User, child: Pupil
):
    await session.execute(
        delete(ParentPupil).where(ParentPupil.parent_id == parent.id, ParentPupil.pupil_id == child.id)
    )
    old_plan = {meal: getattr(child, meal) for meal in MEALS}

    response = await change(client, jwt_settings, parent, child, True, True, True)

    await session.refresh(child)

    assert response.status_code == 403
    assert response.json() == error("UserIsNotParentOfThePupilException", "The user is not a parent of the pupil")

    assert {meal: getattr(child, meal) for meal in MEALS} == old_plan


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, child: Pupil):
    session.add(ParentPupil(parent_id=parent.id, pupil_id=child.id))
    await session.commit()
