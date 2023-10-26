import pytest

from app.users.domain.passwords import InvalidPasswordError, Password


@pytest.mark.parametrize(
    "password",
    [
        "",
    ],
)
def test_invalid_password(password: str):
    with pytest.raises(InvalidPasswordError):
        Password(password)


@pytest.mark.parametrize(
    "password",
    [
        "super_secret_123",
    ],
)
def test_valid_password(password: str):
    Password(password)


def test_hashed_password():
    password, incorrect_password = Password("super_secret_1234"), Password("asdfvq12314ASFD")
    hashed_password = password.hash()

    assert hashed_password != password
    assert hashed_password != password.hash()
    assert hashed_password.verify(password) is True
    assert hashed_password.verify(incorrect_password) is False
