import pytest

from app.account.domain.phone import InvalidPhoneError, Phone


@pytest.mark.parametrize(
    "value",
    [
        "+7 (800) 555-35-35",
    ],
)
def test_phone(value: str):
    Phone(value)


@pytest.mark.parametrize(
    "value",
    [
        "+78005553535",
        "88005553535",
        "a" * 11,
        "8 (800) 555-35-35",
        "+7(800)555-35-35",
        " +7 (800) 555-35-35 ",
        "+7 (80) 55-5-3",
        "+7 (8000) 5555-555-355",
        "+ (800) 555-35-35",
        "+8 (800) 555-35-35",
        "+78 (800) 555-35-35",
    ],
)
def test_incorrect_phone(value: str):
    with pytest.raises(InvalidPhoneError):
        Phone(value)


def test_phone_as_login():
    phone = Phone("+7 (800) 555-35-35")
    login = phone.as_login()

    assert login.value == phone.value
