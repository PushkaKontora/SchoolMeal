import pytest

from app.users.application.services import UserService
from app.users.domain.passwords import Password
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


async def test_logout(access_token: str, user_service: UserService):
    await user_service.logout(access_token)


async def test_logout_many_times(access_token: str, user_service: UserService):
    for _ in range(3):
        await user_service.logout(access_token)


@pytest.fixture
async def access_token(
    parent: User,
    password: Password,
    user_service: UserService,
    secret: str,
) -> str:
    access: AccessToken | None = None

    for _ in range(2):
        access, _ = await user_service.authenticate(parent.login.value, password.value)

    return access.encode(secret)
