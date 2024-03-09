from contextlib import nullcontext

import pytest

from app.shared.domain.personal_info import Email, FullName, Name, Phone


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", False),
        ("Игорь", True),
        ("ИгорЬ", False),
        ("игорь", False),
        ("Игорь1337", False),
        ("@Игорь1337", False),
        ("  Игорь ", False),
        ("И" + "ф" * 63, True),
        ("И" + "ф" * 64, False),
    ],
)
def test_name(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        name = Name(value)

        assert name.value == value[0].upper() + value[1:].lower()


def test_creating_name_using_helper() -> None:
    name = Name.create("ИгОрЬ")

    assert name.value == "Игорь"


def test_creating_full_name_without_patronymic_using_helper() -> None:
    name = FullName.create(last="Дыков", first="Лима")

    assert name.last == Name("Дыков")
    assert name.first == Name("Лима")
    assert name.patronymic is None


def test_creating_full_name_with_patronymic_using_helper() -> None:
    name = FullName.create(last="Дыков", first="Лима", patronymic="Дыкович")

    assert name.last == Name("Дыков")
    assert name.first == Name("Лима")
    assert name.patronymic == Name("Дыкович")


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", False),
        ("serious_dim@google.com", True),
        ("serious-dim@google.com", True),
        ("serious+dim@google.com", True),
        ("peroovy@gmail.com", True),
        ("peroovy@gmail.co", False),
        ("peroovy@busu.com", False),
        ("a@a", False),
        ("1@1", False),
        ("@", False),
        ("name@", False),
        ("@dns", False),
        ("with space@google.com", False),
        ("name@google com", False),
        ("a" * 54 + "@gmail.com", True),
        ("a" * 55 + "@gmail.com", False),
    ],
)
def test_email(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        email = Email(value)

        assert email.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", False),
        ("8005553535", True),
        ("123456789", False),
        ("12345678901", False),
        (" 8005553535 ", False),
        ("-8005553535", False),
        ("A800И5553535@$", False),
    ],
)
def test_phone(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        phone = Phone(value)

        assert phone.value == value
