import pytest
from httpx import AsyncClient, Response
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import JWTSettings
from app.legacy.children.db.child.model import Child
from app.legacy.pupils.db.pupil.model import Pupil
from app.legacy.users.db.user.model import User
from tests.integration.auth.conftest import create_access_token
from tests.integration.children.conftest import child_prefix
from tests.integration.conftest import BearerAuth
from tests.integration.responses import error
from tests.integration.utils import prepare_patch_data


pytestmark = [pytest.mark.integration]

MEALS = ("breakfast", "lunch", "dinner")


async def change(
    client: AsyncClient,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    breakfast: bool | None = None,
    lunch: bool | None = None,
    dinner: bool | None = None,
) -> Response:
    url = child_prefix(pupil.id)
    body = prepare_patch_data({"breakfast": breakfast, "lunch": lunch, "dinner": dinner})
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.patch(url, json=body, auth=BearerAuth(token))


@pytest.mark.parametrize(
    ["plan", "breakfast_init", "lunch_init", "dinner_init"],
    [
        [{}, True, True, True],
        [{"breakfast": True}, False, True, True],
        [{"lunch": True}, True, False, True],
        [{"dinner": True}, True, True, False],
        [{"breakfast": False}, True, True, True],
        [{"lunch": False}, True, True, True],
        [{"dinner": False}, True, True, True],
        [{"breakfast": True, "lunch": True, "dinner": True}, False, False, False],
        [{"breakfast": False, "lunch": False, "dinner": False}, True, True, True],
        [{"breakfast": False, "lunch": False, "dinner": False}, False, False, False],
    ],
    ids=[
        "empty body",
        "enable only breakfast",
        "enable only lunch",
        "enable only dinner",
        "disable only breakfast",
        "disable only lunch",
        "disable only dinner",
        "enable all",
        "disable all",
        "disable already disabled",
    ],
)
async def test_change_meal_plan(
    client: AsyncClient,
    session: AsyncSession,
    jwt_settings: JWTSettings,
    parent: User,
    pupil: Pupil,
    plan: dict,
    breakfast_init: bool,
    lunch_init: bool,
    dinner_init: bool,
):
    pupil.breakfast, pupil.lunch, pupil.dinner = breakfast_init, lunch_init, dinner_init
    session.add(pupil)
    old_plan = {meal: getattr(pupil, meal) for meal in MEALS}
    await session.commit()

    response = await change(client, jwt_settings, parent, pupil, **plan)

    await session.refresh(pupil)
    expected = {meal: plan[meal] if meal in plan else old_plan[meal] for meal in MEALS}

    assert response.status_code == 200
    assert response.json() == expected

    actual = {meal: getattr(pupil, meal) for meal in MEALS}
    assert actual == expected


async def test_change_the_childs_plan_by_some_parent(
    client: AsyncClient, session: AsyncSession, jwt_settings: JWTSettings, parent: User, pupil: Pupil
):
    await session.execute(delete(Child).where(Child.parent_id == parent.id, Child.pupil_id == pupil.id))
    old_plan = {meal: getattr(pupil, meal) for meal in MEALS}

    response = await change(client, jwt_settings, parent, pupil, True, True, True)

    await session.refresh(pupil)

    assert response.status_code == 403
    assert response.json() == error("UserIsNotParentOfThePupilError", "The user is not a parent of the pupil")

    assert {meal: getattr(pupil, meal) for meal in MEALS} == old_plan


@pytest.fixture(autouse=True)
async def prepare_data(session: AsyncSession, parent: User, pupil: Pupil):
    session.add(Child(parent_id=parent.id, pupil_id=pupil.id))
    await session.commit()
