from datetime import date

from app.nutrition.domain.periods import CancellationPeriod, Period, Reason


RowDates = tuple[int, int]
RowPeriod = tuple[int, int, set[str]]


def create_period(start_day: int, end_day: int) -> Period:
    return Period(
        starts_at=create_date(start_day),
        ends_at=create_date(end_day),
    )


def to_row_period(period: Period | None) -> tuple[int, int] | None:
    return (date_as_number(period.starts_at), date_as_number(period.ends_at)) if period else None


def create_cancellation(start_day: int, end_day: int, reasons: set[str]) -> CancellationPeriod:
    return CancellationPeriod(
        starts_at=create_date(start_day),
        ends_at=create_date(end_day),
        reasons=frozenset(map(Reason, reasons)),
    )


def to_row_cancellation(period: CancellationPeriod | None) -> tuple[int, int, set[str]] | None:
    return to_row_period(period) + ({reason.value for reason in period.reasons},) if period else None


def create_date(number: int) -> date:
    return date(year=2023, month=10, day=number)


def date_as_number(date_: date) -> int:
    return date_.day
