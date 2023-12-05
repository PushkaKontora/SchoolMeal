import pytest

from app.users.application.services import UsersService
from app.users.domain.passwords import Password
from app.users.domain.user import User


async def test_getting_user_by_access_token(parent: User, access_token: str, users_service: UsersService):
    user = await users_service.get_user_by_access_token(access_token)

    assert user == parent


@pytest.fixture
async def access_token(
    parent: User,
    password: Password,
    users_service: UsersService,
    secret: str,
) -> str:
    return (
        await users_service.authenticate(
            login=parent.login.value,
            password=password.value,
        )
    )[
        0
    ].encode(secret)
