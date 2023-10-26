import pytest

from app.users.domain.login import Login, LoginIsEmpty


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


def test_empty_login():
    with pytest.raises(LoginIsEmpty):
        Login("")
