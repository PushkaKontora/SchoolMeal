import pytest

from app.users.domain.names import FirstName, InvalidFirstNameError, InvalidLastNameError, LastName


CORRECT_CASES = [
    "Акакий",
    "ЮрЧИК",
    "Акакий Топ",
]

INCORRECT_CASES = [
    "",
    "1337",
    "Акакий1337",
    "Serious",
]


@pytest.mark.parametrize("value", CORRECT_CASES)
def test_first_name(value: str):
    name = FirstName(value)
    assert name.value == value


@pytest.mark.parametrize("value", INCORRECT_CASES)
def test_incorrect_first_name(value: str):
    with pytest.raises(InvalidFirstNameError):
        FirstName(value)


@pytest.mark.parametrize("value", CORRECT_CASES)
def test_last_name(value: str):
    name = LastName(value)
    assert name.value == value


@pytest.mark.parametrize("value", INCORRECT_CASES)
def test_incorrect_last_name(value: str):
    with pytest.raises(InvalidLastNameError):
        LastName(value)
