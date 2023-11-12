import pytest

from app.users.application.services import UserService
from app.users.domain.passwords import Password
from app.users.domain.user import User


async def test_getting_user_by_access_token(parent: User, access_token: str, user_service: UserService):
    user = await user_service.get_user_by_access_token(access_token)

    assert user == parent


@pytest.fixture
async def access_token(
    parent: User,
    password: Password,
    user_service: UserService,
    secret: str,
) -> str:
    return (
        await user_service.authenticate(
            login=parent.login.value,
            password=password.value,
        )
    )[
        0
    ].encode(secret)
