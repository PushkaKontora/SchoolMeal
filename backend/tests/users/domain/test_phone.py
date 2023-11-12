import pytest

from app.users.domain.phone import InvalidPhoneFormat, Phone


def test_phone():
    Phone("+7 (800) 555-35-35")


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
def test_invalid_phone(value: str):
    with pytest.raises(InvalidPhoneFormat):
        Phone(value)


def test_phone_as_login():
    phone = Phone("+7 (800) 555-35-35")
    login = phone.as_login()

    assert login.value == phone.value
