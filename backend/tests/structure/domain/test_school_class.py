from contextlib import nullcontext

import pytest

from app.structure.domain.school_class import Literal, Number


@pytest.mark.parametrize(
    ["value", "is_ok"],
    [
        ("", False),
        *((v, True) for v in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"),
        ("ЖУ", False),
        (" Ж ", False),
        ("1", False),
        ("W", False),
        ("1Ж1", False),
    ],
)
def test_literal(value: str, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        literal = Literal(value)

        assert literal.value == value


@pytest.mark.parametrize(
    ["value", "is_ok"], [(-1, False), (0, False), *((v, True) for v in range(1, 11 + 1)), (12, False)]
)
def test_number(value: int, is_ok: bool) -> None:
    with nullcontext() if is_ok else pytest.raises(ValueError):
        number = Number(value)

        assert number.value == value
