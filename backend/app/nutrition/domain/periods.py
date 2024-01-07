from collections import deque
from collections.abc import Iterable
from dataclasses import field
from datetime import date, timedelta
from itertools import chain
from typing import Iterator, Optional, cast

from pydantic.dataclasses import dataclass

from app.shared.domain.abc import ValueObject


class EndCannotBeGreaterThanStart(Exception):
    pass


class SpecifiedReasonCannotBeEmpty(Exception):
    pass


class ExceededMaxLengthReason(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Reason(ValueObject):
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise SpecifiedReasonCannotBeEmpty

        if len(self.value) > 255:
            raise ExceededMaxLengthReason


@dataclass(eq=True, frozen=True)
class Period(ValueObject):
    starts_at: date
    ends_at: date

    def __post_init_post_parse__(self) -> None:
        if self.starts_at > self.ends_at:
            raise EndCannotBeGreaterThanStart

    def intersect(self, other: "Period") -> Optional["Period"]:
        max_start, min_end = max(self.starts_at, other.starts_at), min(self.ends_at, other.ends_at)

        return Period(starts_at=max_start, ends_at=min_end) if max_start <= min_end else None

    def __contains__(self, item: date) -> bool:
        if not isinstance(item, date):
            raise ValueError("Ожидался тип date")

        return self.starts_at <= item <= self.ends_at


@dataclass(eq=True, frozen=True)
class Day(Period):
    def __init__(self, date_: date) -> None:
        super().__init__(starts_at=date_, ends_at=date_)

    @property
    def date(self) -> date:
        return self.starts_at


@dataclass(eq=True, frozen=True)
class CancellationPeriod(Period):
    reasons: frozenset[Reason]

    def merge(self, other: "CancellationPeriod") -> list["CancellationPeriod"]:
        if not (intersection := self.intersect(other)):
            return []

        result: list[CancellationPeriod] = []
        left, right = min(self, other, key=lambda p: p.starts_at), max(self, other, key=lambda p: p.ends_at)
        reasons = self.reasons | other.reasons

        if intersection.starts_at > left.starts_at:
            result.append(
                CancellationPeriod(
                    starts_at=left.starts_at,
                    ends_at=intersection.starts_at - timedelta(days=1),
                    reasons=left.reasons,
                )
            )

        result.append(
            CancellationPeriod(starts_at=intersection.starts_at, ends_at=intersection.ends_at, reasons=reasons)
        )

        if intersection.ends_at < right.ends_at:
            result.append(
                CancellationPeriod(
                    starts_at=intersection.ends_at + timedelta(days=1),
                    ends_at=right.ends_at,
                    reasons=right.reasons,
                )
            )

        return result

    def exclude(self, period: Period) -> list["CancellationPeriod"]:
        if not (intersection := self.intersect(period)):
            return [self]

        result: list[CancellationPeriod] = []

        if intersection.starts_at > self.starts_at:
            result.append(
                CancellationPeriod(
                    starts_at=self.starts_at,
                    ends_at=intersection.starts_at - timedelta(days=1),
                    reasons=self.reasons,
                )
            )

        if intersection.ends_at < self.ends_at:
            result.append(
                CancellationPeriod(
                    starts_at=intersection.ends_at + timedelta(days=1),
                    ends_at=self.ends_at,
                    reasons=self.reasons,
                )
            )

        return result


@dataclass(eq=True, frozen=True)
class CancellationPeriodSequence(Iterable[CancellationPeriod]):
    periods: tuple[CancellationPeriod, ...] = field(default_factory=tuple)

    def insert(self, period: CancellationPeriod) -> "CancellationPeriodSequence":
        start_insert_idx = self._search_insert_index(period)
        end_insert_idx = start_insert_idx

        new_periods = deque([period])

        while end_insert_idx < len(self.periods):
            previous, next_ = new_periods[-1], cast(CancellationPeriod, self.periods[end_insert_idx])

            if not (merged_periods := previous.merge(next_)):
                break

            new_periods.pop()
            new_periods.extend(merged_periods)
            end_insert_idx += 1

        return CancellationPeriodSequence(
            periods=tuple(
                chain(
                    self.periods[:start_insert_idx],
                    self._combine_periods_with_same_reasons(new_periods),
                    self.periods[end_insert_idx:],
                )
            )
        )

    def remove(self, period: Period) -> "CancellationPeriodSequence":
        start = self._search_insert_index(period)
        end = start

        new_periods: deque[CancellationPeriod] = deque()

        while end < len(self.periods):
            cancellation: CancellationPeriod = self.periods[end]

            if not cancellation.intersect(period):
                break

            new_periods.extend(cancellation.exclude(period))
            end += 1

        return CancellationPeriodSequence(periods=tuple(chain(self.periods[:start], new_periods, self.periods[end:])))

    def _search_insert_index(self, period: Period) -> int:
        left, right = 0, len(self.periods)

        while left < right:
            mid = (left + right) // 2
            left, right = (mid + 1, right) if period.starts_at > self.periods[mid].ends_at else (left, mid)

        return left

    @staticmethod
    def _combine_periods_with_same_reasons(new_periods: deque[CancellationPeriod]) -> Iterable[CancellationPeriod]:
        if not new_periods:
            return

        previous = new_periods.popleft()

        while new_periods:
            current = new_periods.popleft()

            if current.reasons == previous.reasons or min(len(current.reasons), len(previous.reasons)) == 0:
                previous = CancellationPeriod(
                    starts_at=previous.starts_at,
                    ends_at=current.ends_at,
                    reasons=max(current.reasons, previous.reasons, key=len),
                )
                continue

            yield previous
            previous = current

        yield previous

    def __iter__(self) -> Iterator[CancellationPeriod]:
        yield from self.periods
