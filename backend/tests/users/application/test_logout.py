import pytest

from app.users.application.services import UsersService
from app.users.domain.passwords import Password
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


async def test_logout_many_times(access_token: str, users_service: UsersService):
    for _ in range(3):
        await users_service.logout(access_token)


@pytest.fixture
async def access_token(
    parent: User,
    password: Password,
    users_service: UsersService,
    secret: str,
) -> str:
    access: AccessToken | None = None

    for _ in range(2):
        access, _ = await users_service.authenticate(parent.login.value, password.value)

    return access.encode(secret)
