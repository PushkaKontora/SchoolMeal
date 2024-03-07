from contextlib import nullcontext
from datetime import date, datetime, time

import freezegun
import pytest

from app.nutrition.domain.time import (
    YEKATERINBURG,
    Day,
    Period,
    Timeline,
    get_submitting_deadline_within_day,
    has_submitting_deadline_come,
)


RowPeriod = tuple[int, int]


def test_get_submitting_deadline_within_day() -> None:
    day = date(2023, 10, 11)

    deadline = get_submitting_deadline_within_day(day)

    assert deadline.date() == day
    assert deadline.timetz() == time(hour=22, minute=0, second=0, tzinfo=YEKATERINBURG)


@pytest.mark.parametrize(
    ["time_", "is_deadline"],
    [
        (time(hour=19, minute=59), False),
        (time(hour=22, minute=0), True),
        (time(hour=22, minute=0, second=1), True),
    ],
)
def test_has_deadline_submitting_come(time_: time, is_deadline: bool) -> None:
    with freezegun.freeze_time(datetime.combine(date.today(), time_, tzinfo=YEKATERINBURG)):
        assert has_submitting_deadline_come(date.today()) == is_deadline


@pytest.mark.parametrize(["start", "end", "is_ok"], [[2, 1, False], [2, 2, True], [2, 3, True]])
def test_period(start: int, end: int, is_ok: bool) -> None:
    starts_at, ends_at = _create_date(start), _create_date(end)

    with nullcontext() if is_ok else pytest.raises(ValueError):
        period = Period(start=starts_at, end=ends_at)

        assert period.start == starts_at
        assert period.end == ends_at


def test_day() -> None:
    day = Day(date(2023, 10, 23))

    assert day.start == day.end


def test_day_gt() -> None:
    assert Day(date(2023, 1, 2)) > Day(date(2023, 1, 1))
    assert not (Day(date(2023, 1, 2)) > Day(date(2023, 1, 2)))
    assert not (Day(date(2023, 1, 2)) > Day(date(2023, 1, 3)))


def test_day_lt() -> None:
    assert not (Day(date(2023, 1, 2)) < Day(date(2023, 1, 1)))
    assert not (Day(date(2023, 1, 2)) < Day(date(2023, 1, 2)))
    assert Day(date(2023, 1, 2)) < Day(date(2023, 1, 3))


def test_day_ge() -> None:
    assert Day(date(2023, 1, 2)) >= Day(date(2023, 1, 1))
    assert Day(date(2023, 1, 2)) >= Day(date(2023, 1, 2))
    assert not (Day(date(2023, 1, 2)) >= Day(date(2023, 1, 3)))


def test_day_le() -> None:
    assert not (Day(date(2023, 1, 2)) <= Day(date(2023, 1, 1)))
    assert Day(date(2023, 1, 2)) <= Day(date(2023, 1, 2))
    assert Day(date(2023, 1, 2)) <= Day(date(2023, 1, 3))


@pytest.mark.parametrize(
    ["start", "end", "expected"],
    [
        (1, 1, [1]),
        (1, 3, [1, 2, 3]),
    ],
)
def test_period_iterator(start: int, end: int, expected: list[int]) -> None:
    period = _create_period(start_day=start, end_day=end)

    for i, day in enumerate(period):
        assert day.day == expected[i]


@pytest.mark.parametrize(
    ["a_", "b_", "expected"],
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
def test_intersecting(a_: RowPeriod, b_: RowPeriod, expected: RowPeriod | None) -> None:
    a, b = _create_period(*a_), _create_period(*b_)

    assert a.intersects(b) == b.intersects(a) == (_create_period(*expected) if expected else None)


@pytest.mark.parametrize(
    ["periods", "expected"],
    [
        [[(1, 3)], [(1, 3)]],
        [[(1, 3), (4, 10)], [(1, 10)]],
        [[(4, 10), (1, 3)], [(1, 10)]],
        [[(1, 1), (2, 2)], [(1, 2)]],
        [[(2, 2), (1, 1)], [(1, 2)]],
        [[(1, 5), (3, 7)], [(1, 7)]],
        [[(3, 7), (1, 5)], [(1, 7)]],
        [[(1, 5), (2, 3)], [(1, 5)]],
        [[(2, 3), (1, 5)], [(1, 5)]],
        [[(1, 3), (1, 3)], [(1, 3)]],
        [[(1, 3), (3, 5)], [(1, 5)]],
        [[(1, 5), (5, 5)], [(1, 5)]],
        [[(1, 5), (3, 3)], [(1, 5)]],
        [[(1, 5), (1, 1)], [(1, 5)]],
        [
            [(1, 1), (1, 4), (3, 10), (3, 15), (20, 30), (5, 10), (8, 15), (13, 18), (10, 10), (10, 14)],
            [(1, 18), (20, 30)],
        ],
    ],
)
def test_inserting_in_timeline(periods: list[RowPeriod], expected: list[RowPeriod]) -> None:
    timeline = Timeline()

    for start, end in periods:
        timeline.insert(_create_period(start, end))

    assert list(timeline) == [_create_period(start, end) for start, end in expected]


@pytest.mark.parametrize(
    ["periods", "period", "expected"],
    [
        [[(1, 10)], (5, 5), [(1, 4), (6, 10)]],
        [[(1, 10)], (4, 6), [(1, 3), (7, 10)]],
        [[(1, 10)], (2, 9), [(1, 1), (10, 10)]],
        [[(1, 10)], (1, 10), []],
        [[(5, 10)], (1, 20), []],
        [[(3, 5), (10, 15)], (6, 9), [(3, 5), (10, 15)]],
        [[(3, 5), (10, 15)], (5, 10), [(3, 4), (11, 15)]],
        [[(3, 5), (10, 15)], (4, 14), [(3, 3), (15, 15)]],
        [[(3, 5), (10, 15)], (3, 15), []],
    ],
)
def test_excluding_from_timeline(periods: list[RowPeriod], period: RowPeriod, expected: list[RowPeriod]) -> None:
    timeline = Timeline()

    for start, end in periods:
        timeline.insert(_create_period(start, end))

    timeline.exclude(_create_period(*period))

    assert list(timeline) == [_create_period(start, end) for start, end in expected]


def _create_period(start_day: int, end_day: int) -> Period:
    return Period(
        start=date(year=2023, month=10, day=start_day),
        end=date(year=2023, month=10, day=end_day),
    )


def _to_row_period(period: Period | None) -> RowPeriod | None:
    return (period.start.day, period.end.day) if period else None


def _create_date(number: int) -> date:
    return date(year=2023, month=10, day=number)
