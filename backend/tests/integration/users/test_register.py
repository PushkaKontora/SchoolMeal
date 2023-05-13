import bcrypt
import freezegun
import pytest
from httpx import AsyncClient, Response
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.db.password.model import Password
from app.users.db.user.model import Role, User
from tests.integration.responses import error
from tests.integration.users.conftest import USERS_PREFIX
from tests.integration.utils import datetime_to_str


pytestmark = [pytest.mark.integration]


URL = USERS_PREFIX


async def register(
    client: AsyncClient, phone: str, password: str, last_name: str, first_name: str, email: str | None = None
) -> Response:
    return await client.post(
        URL,
        json={
            "phone": phone,
            "password": password,
            "lastName": last_name,
            "firstName": first_name,
            "email": email,
        },
    )


@freezegun.freeze_time()
async def test_register_parent(
    client: AsyncClient,
    session: AsyncSession,
    phone="+78005553535",
    password="very secret",
    last_name="Dykov",
    first_name="Lima",
    email="email@email.com",
):
    response = await register(client, phone, password, last_name, first_name, email)

    assert response.status_code == 201

    user: User = (await session.execute(select(User).where(User.login == phone))).scalar_one()
    assert user.last_name == last_name
    assert user.first_name == first_name
    assert user.email == email
    assert user.phone == phone

    hashed_password: Password = (
        await session.execute(select(Password).where(Password.user_id == user.id))
    ).scalar_one()
    assert bcrypt.checkpw(password.encode("utf-8"), hashed_password.value)

    assert response.json() == {
        "id": user.id,
        "lastName": last_name,
        "firstName": first_name,
        "phone": phone,
        "email": email,
        "login": phone,
        "createdAt": datetime_to_str(user.created_at),
        "role": Role.PARENT.value,
        "photoPath": None,
    }


@pytest.mark.parametrize(
    ["phone", "is_valid"],
    [
        ["+78005553535", True],
        ["78005553535", False],
        ["+7" + "0" * 9, False],
        ["+7" + "0" * 11, False],
        ["88005553535", False],
        ["+7 (800) 555 35 35", False],
        ["", False],
        [None, False],
    ],
    ids=[
        "correct phone",
        "missed a plus",
        "number of digits is less than 11",
        "number of digits is greater than 11",
        "missed a plus and first digit is 8",
        "contains not just digits and a plus",
        "empty",
        "null",
    ],
)
async def test_validation_phone(client: AsyncClient, session: AsyncSession, phone: str, is_valid: bool):
    await _test_validation(client, session, phone, "email@email.com", is_valid)


@pytest.mark.parametrize(
    ["email", "is_valid"],
    [
        ["email@email.com", True],
        [None, True],
        ["email@", False],
        ["emailemail.com", False],
        ["@email.com", False],
    ],
    ids=["correct email", "null", "messed a hostname", "missed @", "missed mailbox"],
)
async def test_validation_email(client: AsyncClient, session: AsyncSession, email: str, is_valid: bool):
    await _test_validation(client, session, "+78005553535", email, is_valid)


async def _test_validation(
    client: AsyncClient, session: AsyncSession, phone: str | None, email: str | None, is_valid: bool
):
    response = await register(client, phone, "secret", "Dykov", "Lima", email)

    count = 1 if is_valid else 0
    code = 201 if is_valid else 422

    assert response.status_code == code
    assert await session.scalar(select(func.count()).select_from(User)) == count
    assert await session.scalar(select(func.count()).select_from(Password)) == count


@pytest.mark.parametrize(
    ["phone", "email"],
    [
        ["+78005553535", "unique@email.com"],
        ["+71111111111", "email@email.com"],
        ["+78005553535", "email@email.com"],
    ],
    ids=[
        "not unique phone",
        "not unique email",
        "not unique phone and email",
    ],
)
async def test_unique_constraint_on_phone_and_email(
    client: AsyncClient, session: AsyncSession, phone: str, email: str, parent
):
    parent.login = parent.phone = "+78005553535"
    parent.email = "email@email.com"
    await session.commit()

    response = await register(client, phone, "secret", "Dykov", "Lima", email)

    assert response.status_code == 400
    assert response.json() == error("NonUniqueUserDataError", "Login, phone or email should be unique")
    assert await session.scalar(select(func.count()).select_from(User)) == 1
