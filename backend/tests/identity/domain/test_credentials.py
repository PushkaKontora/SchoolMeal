from contextlib import nullcontext

import pytest

from app.identity.domain.credentials import Login, Password


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", False),
        ("super_boy", True),
    ],
)
def test_login(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        login = Login(value)

        assert login.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ["", False],
        ["P@ssw0r", False],
        ["P@ssw0rd", True],
        ["P@a0" + "1" * 26, True],
        ["P@a0" + "1" * 27, False],
        ["p@ssw0rd1234", False],
        ["P@SSW0RD1234", False],
        ["P@ssw界rd1234", False],
        ["P@ssword", False],
        ["P@ssw0rd 1234", False],
        ["P@ssword`=1234", False],
    ],
)
def test_password(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        password = Password(value)

        assert password.value == value


def test_hashed_password():
    a, b = Password("P@ssw0rd1337"), Password("P@ssw0rd228")
    hashed_a = a.hash()

    assert hashed_a != a
    assert hashed_a != a.hash()
    assert hashed_a.verify(a) is True
    assert hashed_a.verify(b) is False
