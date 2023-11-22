from contextlib import nullcontext
from datetime import date

import pytest

from app.nutrition.domain.periods import (
    CancellationPeriod,
    CancellationPeriodSequence,
    EndCannotBeGreaterThanStart,
    Period,
    SpecifiedReason,
)


RowDates = tuple[int, int]
RowPeriod = tuple[int, int, set[str]]


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
        CancellationPeriod(starts_at=_create_date(start_day), ends_at=_create_date(end_day), reasons=frozenset())


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
    a_period, b_period = _create_period(*a), _create_period(*b)

    assert _to_row_period(a_period.intersect(b_period)) == expected
    assert _to_row_period(b_period.intersect(a_period)) == expected


@pytest.mark.parametrize(
    ["items", "expected"],
    [
        (permutation, expected)
        for items, expected in [
            [
                [(1, 3, {"a"})],
                [(1, 3, {"a"})],
            ],
            [
                [(1, 3, {"a"}), (5, 8, {"b"})],
                [(1, 3, {"a"}), (5, 8, {"b"})],
            ],
            [
                [(1, 6, {"a"}), (3, 8, {"b"})],
                [(1, 2, {"a"}), (3, 6, {"a", "b"}), (7, 8, {"b"})],
            ],
            [
                [(1, 6, {"a"}), (3, 8, {"a"})],
                [(1, 8, {"a"})],
            ],
            [
                [(1, 6, {"a"}), (3, 8, {})],
                [(1, 8, {"a"})],
            ],
            [
                [(1, 8, {"a"}), (3, 5, {"b"})],
                [(1, 2, {"a"}), (3, 5, {"a", "b"}), (6, 8, {"a"})],
            ],
            [
                [(1, 8, {"a"}), (3, 5, {"a"})],
                [(1, 8, {"a"})],
            ],
            [
                [(1, 8, {"a"}), (3, 5, {})],
                [(1, 8, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (1, 5, {"b"})],
                [(1, 5, {"a", "b"})],
            ],
            [
                [(1, 5, {"a"}), (1, 5, {"a"})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (1, 5, {})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (3, 3, {"b"})],
                [(1, 2, {"a"}), (3, 3, {"a", "b"}), (4, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (3, 3, {"a"})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (3, 3, {})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 1, {"a"}), (1, 5, {"b"})],
                [(1, 1, {"a", "b"}), (2, 5, {"b"})],
            ],
            [
                [(1, 1, {"a"}), (1, 5, {"a"})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 1, {"a"}), (1, 5, {})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (5, 5, {"b"})],
                [(1, 4, {"a"}), (5, 5, {"a", "b"})],
            ],
            [
                [(1, 5, {"a"}), (5, 5, {"a"})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (5, 5, {})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 1, {"a"}), (1, 1, {"b"})],
                [(1, 1, {"a", "b"})],
            ],
            [
                [(1, 1, {"a"}), (1, 1, {"a"})],
                [(1, 1, {"a"})],
            ],
            [
                [(1, 1, {"a"}), (1, 1, {})],
                [(1, 1, {"a"})],
            ],
            [
                [(1, 1, {"a"}), (2, 3, {"b"})],
                [(1, 1, {"a"}), (2, 3, {"b"})],
            ],
            [
                [(1, 1, {"a"}), (2, 3, {"a"})],
                [(1, 1, {"a"}), (2, 3, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (2, 4, {"b"}), (3, 3, {"c"})],
                [(1, 1, {"a"}), (2, 2, {"a", "b"}), (3, 3, {"a", "b", "c"}), (4, 4, {"a", "b"}), (5, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (2, 4, {"a"}), (3, 3, {"a"})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {}), (2, 4, {"a"}), (3, 3, {})],
                [(1, 5, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (5, 8, {"b"}), (8, 10, {"c"})],
                [(1, 4, {"a"}), (5, 5, {"a", "b"}), (6, 7, {"b"}), (8, 8, {"b", "c"}), (9, 10, {"c"})],
            ],
            [
                [(1, 5, {"a"}), (5, 8, {"a"}), (8, 10, {"a"})],
                [(1, 10, {"a"})],
            ],
            [
                [(1, 5, {}), (5, 8, {"a"}), (8, 10, {})],
                [(1, 10, {"a"})],
            ],
            [
                [(1, 5, {"a"}), (5, 8, {"a", "b"})],
                [(1, 4, {"a"}), (5, 8, {"a", "b"})],
            ],
            [
                [(1, 9, {"a"}), (5, 11, "b"), (5, 13, "c"), (9, 9, "d"), (9, 15, "e"), (9, 9, "f"), (11, 11, "g")],
                [
                    (1, 4, {"a"}),
                    (5, 8, {"b", "a", "c"}),
                    (9, 9, {"a", "d", "b", "e", "c", "f"}),
                    (10, 10, {"b", "e", "c"}),
                    (11, 11, {"b", "e", "c", "g"}),
                    (12, 13, {"e", "c"}),
                    (14, 15, {"e"}),
                ],
            ],
            [
                [
                    (1, 9, {"a"}),
                    (5, 11, {"a"}),
                    (5, 13, {"a"}),
                    (9, 9, {"a"}),
                    (9, 15, {"a"}),
                    (9, 9, {"a"}),
                    (11, 11, {"a"}),
                ],
                [(1, 15, {"a"})],
            ],
            [
                [(1, 9, {"a"}), (5, 11, {"b"}), (9, 15, {"b"}), (5, 13, {"b", "c"}), (9, 9, {})],
                [(1, 4, {"a"}), (5, 9, {"a", "b", "c"}), (10, 13, {"b", "c"}), (14, 15, {"b"})],
            ],
        ]
        for permutation in [items, list(reversed(items))]
    ],
)
def test_inserting_period_to_sequence(items: list[RowPeriod], expected: list[RowPeriod]):
    sequence = CancellationPeriodSequence()

    for start, end, reasons in items:
        sequence = sequence.insert(_create_cancellation(start, end, reasons))

    assert [_to_row_cancellation(period) for period in sequence] == expected


def _create_period(start_day: int, end_day: int) -> Period:
    return Period(
        starts_at=_create_date(start_day),
        ends_at=_create_date(end_day),
    )


def _to_row_period(period: Period | None) -> tuple[int, int] | None:
    return (_date_as_number(period.starts_at), _date_as_number(period.ends_at)) if period else None


def _create_cancellation(start_day: int, end_day: int, reasons: set[str]) -> CancellationPeriod:
    return CancellationPeriod(
        starts_at=_create_date(start_day),
        ends_at=_create_date(end_day),
        reasons=frozenset(map(SpecifiedReason, reasons)),
    )


def _to_row_cancellation(period: CancellationPeriod | None) -> tuple[int, int, set[str]] | None:
    return _to_row_period(period) + ({reason.value for reason in period.reasons},) if period else None


def _create_date(number: int) -> date:
    return date(year=2023, month=10, day=number)


def _date_as_number(date_: date) -> int:
    return date_.day
