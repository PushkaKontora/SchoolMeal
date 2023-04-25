import pytest
from httpx import AsyncClient, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.children.db.models import ParentPupil
from app.config import JWTSettings
from app.pupils.db.models import Pupil
from app.users.db.models import Role, User
from tests.auth.integration.conftest import create_access_token
from tests.children.integration.conftest import CHILDREN_PREFIX
from tests.conftest import BearerAuth
from tests.responses import SUCCESS, error


pytestmark = [pytest.mark.integration]

URL = CHILDREN_PREFIX


async def add_child(client: AsyncClient, parent: User, child: Pupil, jwt_settings: JWTSettings) -> Response:
    token = create_access_token(parent.id, parent.role, jwt_settings)

    return await client.post(URL, json={"childId": child.id}, auth=BearerAuth(token))


@pytest.mark.parametrize("role", Role)
async def test_any_user_can_add_child(
    client: AsyncClient, session: AsyncSession, parent: User, role: Role, child: Pupil, jwt_settings: JWTSettings
):
    parent.role = role
    await session.commit()

    response = await add_child(client, parent, child, jwt_settings)

    assert response.status_code == 200
    assert response.json() == SUCCESS

    children = await session.scalars(
        select(ParentPupil).with_only_columns(ParentPupil.pupil_id).where(ParentPupil.parent_id == parent.id)
    )
    assert list(children) == [child.id]


async def test_child_can_be_added_by_multiple_parents(
    client: AsyncClient,
    session: AsyncSession,
    parent: User,
    another_parent: User,
    child: Pupil,
    jwt_settings: JWTSettings,
):
    session.add(ParentPupil(parent_id=another_parent.id, pupil_id=child.id))
    await session.commit()

    response = await add_child(client, parent, child, jwt_settings)

    assert response.status_code == 200
    assert response.json() == SUCCESS

    parent_children = await session.scalars(
        select(ParentPupil).with_only_columns(ParentPupil.pupil_id).where(ParentPupil.parent_id == parent.id)
    )
    another_parent_children = await session.scalars(
        select(ParentPupil).with_only_columns(ParentPupil.pupil_id).where(ParentPupil.parent_id == another_parent.id)
    )
    assert list(parent_children) == [child.id]
    assert list(another_parent_children) == [child.id]


async def test_unknown_user_cannot_add_child(
    client: AsyncClient, session: AsyncSession, parent: User, child: Pupil, jwt_settings: JWTSettings
):
    await session.delete(parent)
    await session.commit()

    response = await add_child(client, parent, child, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotFoundParentException", "The parent was not found")

    children_count = await session.scalar(
        select(ParentPupil).with_only_columns(func.count()).where(ParentPupil.parent_id == parent.id)
    )
    assert children_count == 0


async def test_parent_cannot_add_unknown_child(
    client: AsyncClient, session: AsyncSession, parent: User, child: Pupil, jwt_settings: JWTSettings
):
    await session.delete(child)
    await session.commit()

    response = await add_child(client, parent, child, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotFoundChildException", "The child was not found")

    children_count = await session.scalar(
        select(ParentPupil).with_only_columns(func.count()).where(ParentPupil.parent_id == parent.id)
    )
    assert children_count == 0


async def test_user_add_child_that_was_added_by_him(
    client: AsyncClient, session: AsyncSession, parent: User, child: Pupil, jwt_settings: JWTSettings
):
    session.add(ParentPupil(parent_id=parent.id, pupil_id=child.id))
    await session.commit()

    response = await add_child(client, parent, child, jwt_settings)

    assert response.status_code == 400
    assert response.json() == error("NotUniqueChildException", "The child was already added by the user")

    children_count = await session.scalar(
        select(ParentPupil).with_only_columns(func.count()).where(ParentPupil.parent_id == parent.id)
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
