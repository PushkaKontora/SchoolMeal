from contextlib import nullcontext

import pytest

from app.nutrition.domain.periods import EndCannotBeGreaterThanStart, Period
from tests.nutrition.domain.periods.utils import RowDates, create_date, create_period, to_row_period


@pytest.mark.parametrize(
    ["start_day", "end_day", "error"],
    [
        [2, 2, None],
        [2, 3, None],
        [2, 1, EndCannotBeGreaterThanStart],
    ],
)
def test_creating_period(start_day: int, end_day: int, error: type[Exception] | None):
    ctx = nullcontext() if error is None else pytest.raises(error)

    with ctx:
        Period(starts_at=create_date(start_day), ends_at=create_date(end_day))


@pytest.mark.parametrize(
    ["a", "b", "expected"],
    [
        [(1, 10), (10, 12), (10, 10)],
        [(1, 2), (1, 2), (1, 2)],
        [(1, 1), (1, 1), (1, 1)],
        [(1, 10), (5, 6), (5, 6)],
        [(1, 6), (4, 10), (4, 6)],
        [(1, 1), (2, 2), None],
        [(1, 5), (6, 6), None],
        [(1, 3), (4, 5), None],
    ],
)
def test_intersection_periods(a: RowDates, b: RowDates, expected: RowDates | None):
    a_period, b_period = create_period(*a), create_period(*b)

    assert to_row_period(a_period.intersect(b_period)) == expected
    assert to_row_period(b_period.intersect(a_period)) == expected
