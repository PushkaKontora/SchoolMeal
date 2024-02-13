import pytest

from app.nutrition.domain.school_class import ClassID, Literal, Number
from app.shared.exceptions import DomainException


@pytest.mark.parametrize("value", [*map(chr, range(ord("А"), ord("Я") + 1)), "Ё"])
def test_valid_literal(value: str) -> None:
    literal = Literal(value)

    assert literal.value == value


@pytest.mark.parametrize("value", ["G", "г", "1", ""])
def test_invalid_literal(value: str) -> None:
    with pytest.raises(DomainException):
        Literal(value)


@pytest.mark.parametrize("value", range(1, 11 + 1))
def test_valid_number(value: int) -> None:
    number = Number(value)

    assert number.value == value


@pytest.mark.parametrize("value", [-1, 0, 12])
def test_invalid_number(value: int) -> None:
    with pytest.raises(DomainException):
        Number(value)


def test_generation_unique_class_id() -> None:
    assert ClassID.generate() != ClassID.generate()
