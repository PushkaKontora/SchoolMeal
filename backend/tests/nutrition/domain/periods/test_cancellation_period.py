import pytest

from tests.nutrition.domain.periods.utils import RowDates, create_cancellation, create_period, to_row_cancellation


@pytest.mark.parametrize(
    ["period", "exclude", "expected"],
    [
        [(1, 5), (6, 6), [(1, 5)]],
        [(1, 5), (5, 5), [(1, 4)]],
        [(1, 5), (3, 3), [(1, 2), (4, 5)]],
        [(1, 3), (2, 2), [(1, 1), (3, 3)]],
        [(1, 5), (1, 1), [(2, 5)]],
        [(2, 5), (1, 1), [(2, 5)]],
        [(1, 1), (1, 1), []],
        [(1, 1), (2, 2), [(1, 1)]],
        [(1, 10), (3, 5), [(1, 2), (6, 10)]],
        [(1, 5), (3, 10), [(1, 2)]],
        [(2, 3), (1, 10), []],
    ],
)
def test_excluding(period: RowDates, exclude: RowDates, expected: list[RowDates]):
    cancellation = create_cancellation(*period, reasons={"a", "b"})

    result = cancellation.exclude(create_period(*exclude))

    assert [to_row_cancellation(r) for r in result] == [e + ({"a", "b"},) for e in expected]
