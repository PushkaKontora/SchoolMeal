import pytest

from app.utils.string import camelize_snakecase


@pytest.mark.unit
@pytest.mark.parametrize(
    ["string", "expected"],
    [
        ["one", "one"],
        ["one_two", "oneTwo"],
        ["oneTwo", "oneTwo"],
    ],
)
def test_camelize_snakecase(string: str, expected: str):
    actual = camelize_snakecase(string)

    assert actual == expected
