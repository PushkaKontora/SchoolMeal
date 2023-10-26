from uuid import UUID

import pytest
from freezegun import freeze_time

from app.account.application.repositories import ICredentialsRepository, ISessionsRepository
from app.account.application.use_cases.jwt import IncorrectLoginOrPasswordError, authenticate
from app.account.domain.login import Login
from app.account.domain.passwords import Password
from tests.account.application.tokens import validate_tokens


@freeze_time()
async def test_authentication(
    credential_id: UUID,
    login: Login,
    password: Password,
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
):
    access, refresh = await authenticate(login, password, credentials_repository, sessions_repository)

    validate_tokens(access, refresh, expected_credential_id=credential_id)


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
    credentials_repository: ICredentialsRepository,
    sessions_repository: ISessionsRepository,
):
    with pytest.raises(IncorrectLoginOrPasswordError) as error:
        await authenticate(Login(login_), Password(password_), credentials_repository, sessions_repository)

    assert str(error.value) == "Неправильный логин или пароль"
