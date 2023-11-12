import pytest

from app.users.domain.names import (
    FirstName,
    FirstNameContainsNotCyrillicCharacters,
    LastName,
    LastNameContainsNotCyrillicCharacters,
)


NAMES_CONTAINING_ONLY_CYRILLIC = [
    "Акакий",
    "ЮрЧИК",
    "Акакий Топ",
]

INCORRECT_NAMES = [
    "",
    "1337",
    "Акакий1337",
    "Serious",
]


@pytest.mark.parametrize("value", NAMES_CONTAINING_ONLY_CYRILLIC)
def test_first_name(value: str):
    name = FirstName(value)
    assert name.value == value


@pytest.mark.parametrize("value", INCORRECT_NAMES)
def test_first_name_containing_non_cyrillic(value: str):
    with pytest.raises(FirstNameContainsNotCyrillicCharacters):
        FirstName(value)


@pytest.mark.parametrize("value", NAMES_CONTAINING_ONLY_CYRILLIC)
def test_last_name(value: str):
    name = LastName(value)
    assert name.value == value


@pytest.mark.parametrize("value", INCORRECT_NAMES)
def test_last_name_containing_non_cyrillic(value: str):
    with pytest.raises(LastNameContainsNotCyrillicCharacters):
        LastName(value)
