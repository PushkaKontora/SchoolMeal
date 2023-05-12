import pytest
from httpx import AsyncClient, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.children.db.child.model import Child
from app.config import JWTSettings
from app.pupils.db.pupil.model import Pupil
from app.users.db.user.model import Role, User
from tests.integration.auth.conftest import create_access_token
from tests.integration.children.conftest import CHILDREN_PREFIX
from tests.integration.conftest import BearerAuth
from tests.integration.responses import SUCCESS, error


pytestmark = [pytest.mark.integration]

URL = CHILDREN_PREFIX


async def add_child(client: AsyncClient, parent: User, pupil: Pupil, jwt_settings: JWTSettings) -> Response:
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.post(URL, json={"childId": pupil.id}, auth=BearerAuth(token))


@pytest.mark.parametrize("role", Role)
async def test_any_user_can_add_child(
    client: AsyncClient, session: AsyncSession, parent: User, role: Role, pupil: Pupil, jwt_settings: JWTSettings
):
    parent.role = role
    await session.commit()

    response = await add_child(client, parent, pupil, jwt_settings)

    assert response.status_code == 200, response.text
    assert response.json() == SUCCESS

    children = await session.scalars(
        select(Child).with_only_columns(Child.pupil_id).where(Child.parent_id == parent.id)
    )
    assert list(children) == [pupil.id]


async def test_child_can_be_added_by_multiple_parents(
    client: AsyncClient,
    session: AsyncSession,
    parent: User,
    another_parent: User,
    pupil: Pupil,
    jwt_settings: JWTSettings,
):
    session.add(Child(parent_id=another_parent.id, pupil_id=pupil.id))
    await session.commit()

    response = await add_child(client, parent, pupil, jwt_settings)

    assert response.status_code == 200
    assert response.json() == SUCCESS

    parent_children = await session.scalars(
        select(Child).with_only_columns(Child.pupil_id).where(Child.parent_id == parent.id)
    )
    another_parent_children = await session.scalars(
        select(Child).with_only_columns(Child.pupil_id).where(Child.parent_id == another_parent.id)
    )
    assert list(parent_children) == [pupil.id]
    assert list(another_parent_children) == [pupil.id]


async def test_unknown_user_cannot_add_child(
    client: AsyncClient, session: AsyncSession, parent: User, pupil: Pupil, jwt_settings: JWTSettings
):
    await session.delete(parent)
    await session.commit()

    response = await add_child(client, parent, pupil, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotFoundParentError", "The parent was not found")

    children_count = await session.scalar(
        select(Child).with_only_columns(func.count()).where(Child.parent_id == parent.id)
    )
    assert children_count == 0


async def test_parent_cannot_add_unknown_child(
    client: AsyncClient, session: AsyncSession, parent: User, pupil: Pupil, jwt_settings: JWTSettings
):
    await session.delete(pupil)
    await session.commit()

    response = await add_child(client, parent, pupil, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotFoundChildError", "The child was not found")

    children_count = await session.scalar(
        select(Child).with_only_columns(func.count()).where(Child.parent_id == parent.id)
    )
    assert children_count == 0


async def test_user_add_child_that_was_added_by_him(
    client: AsyncClient, session: AsyncSession, parent: User, pupil: Pupil, jwt_settings: JWTSettings
):
    session.add(Child(parent_id=parent.id, pupil_id=pupil.id))
    await session.commit()

    response = await add_child(client, parent, pupil, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotUniqueChildError", "The child was already added by the user")

    children_count = await session.scalar(
        select(Child).with_only_columns(func.count()).where(Child.parent_id == parent.id)
    )
    assert children_count == 1


@pytest.fixture
async def another_parent(session: AsyncSession) -> User:
    user = User(
        last_name="Samkov",
        first_name="Nikita",
        login="qwerqfxcvzxcv",
        role=Role.PARENT,
        phone="+78995553515",
        email="super@pro.com",
        photo_path=r"https://yandex.ru/images/asdfwerqwe",
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
