import pytest
from freezegun import freeze_time

from app.users.application.repositories import ISessionsRepository, IUsersRepository
from app.users.application.use_cases.jwt import IncorrectLoginOrPasswordError, authenticate
from app.users.domain.login import Login
from app.users.domain.passwords import Password
from app.users.domain.user import User
from tests.users.application.tokens import validate_tokens


@freeze_time()
async def test_authentication(
    parent: User,
    password: Password,
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
):
    access, refresh = await authenticate(parent.login, password, users_repository, sessions_repository)

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
    users_repository: IUsersRepository,
    sessions_repository: ISessionsRepository,
):
    with pytest.raises(IncorrectLoginOrPasswordError) as error:
        await authenticate(Login(login_), Password(password_), users_repository, sessions_repository)

    assert str(error.value) == "Неправильный логин или пароль"
