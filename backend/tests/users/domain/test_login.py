import pytest

from app.users.domain.login import InvalidLoginError, Login


@pytest.mark.parametrize(
    "login",
    [
        "username",
        "+78005553535",
        "+7982",
    ],
)
def test_valid_login(login: str):
    Login(login)


@pytest.mark.parametrize(
    "login",
    [
        "",
    ],
)
def test_invalid_login(login: str):
    with pytest.raises(InvalidLoginError):
        Login(login)
