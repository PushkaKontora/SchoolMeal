import pytest

from app.users.domain.passwords import (
    Password,
    PasswordContainsUnavailableSpecialCharacter,
    PasswordDoesntContainDigit,
    PasswordDoesntContainLowerLetter,
    PasswordDoesntContainUpperLetter,
    PasswordIsEmpty,
    PasswordIsLong,
    PasswordIsShort,
    PasswordMustContainOnlyASCIILetter,
    PasswordMustNotContainSpaces,
    StrictPassword,
)


def test_empty_password():
    with pytest.raises(PasswordIsEmpty):
        Password("")


def test_valid_strict_password():
    StrictPassword("P@ssw0rd1234")


@pytest.mark.parametrize(
    ["value", "error"],
    [
        ["", PasswordIsEmpty],
        ["P@s12", PasswordIsShort],
        ["P@s12" * 129, PasswordIsLong],
        ["p@ssw0rd1234", PasswordDoesntContainUpperLetter],
        ["P@SSW0RD1234", PasswordDoesntContainLowerLetter],
        ["P@ssw界rd1234", PasswordMustContainOnlyASCIILetter],
        ["P@ssword", PasswordDoesntContainDigit],
        ["P@ssw0rd 1234", PasswordMustNotContainSpaces],
        ["P@ssword`=1234", PasswordContainsUnavailableSpecialCharacter],
    ],
)
def test_invalid_strict_password(value: str, error: type[Exception]):
    with pytest.raises(error):
        StrictPassword(value)


def test_hashed_password():
    password, incorrect_password = Password("super_secret_1234"), Password("asdfvq12314ASFD")
    hashed_password = password.hash()

    assert hashed_password != password
    assert hashed_password != password.hash()
    assert hashed_password.verify(password) is True
    assert hashed_password.verify(incorrect_password) is False
