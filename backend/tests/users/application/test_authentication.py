import pytest
from freezegun import freeze_time

from app.users.application.services import IncorrectLoginOrPassword, UserService
from app.users.domain.passwords import Password
from app.users.domain.user import User
from tests.users.application.tokens import validate_tokens


@freeze_time()
async def test_authentication(parent: User, password: Password, user_service: UserService):
    access, refresh = await user_service.authenticate(parent.login.value, password.value)

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
    user_service: UserService,
):
    with pytest.raises(IncorrectLoginOrPassword):
        await user_service.authenticate(login_, password_)
