import pytest
from freezegun import freeze_time

from app.users.application.services import IncorrectLoginOrPassword, UsersService
from app.users.domain.passwords import Password
from app.users.domain.user import User
from tests.users.application.tokens import validate_tokens


@freeze_time()
async def test_authentication(parent: User, password: Password, users_service: UsersService):
    access, refresh = await users_service.authenticate(parent.login.value, password.value)

    validate_tokens(access, refresh, expected_user_id=parent.id)


@pytest.mark.parametrize(
    ["login_", "password_"],
    [
        ["incorrect", "P@ssw0rd1234"],
        ["username", "incorrect"],
        ["incorrect", "incorrect"],
    ],
)
async def test_authentication_using_incorrect_credentials(
    login_: str,
    password_: str,
    users_service: UsersService,
):
    with pytest.raises(IncorrectLoginOrPassword):
        await users_service.authenticate(login_, password_)
