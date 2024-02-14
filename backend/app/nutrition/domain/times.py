from collections import deque
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import Iterable, Iterator, Optional

from app.shared.exceptions import DomainException


yekaterinburg = timezone(offset=timedelta(hours=5), name="Yekaterinburg")


def now() -> datetime:
    return datetime.now(tz=yekaterinburg)


def combine(day: date, time_: time) -> datetime:
    return datetime.combine(day, time_, tzinfo=yekaterinburg)


@dataclass(frozen=True, eq=True)
class Period:
    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise DomainException("Дата начала периода не может быть больше даты окончания")

    def intersects(self, other: "Period") -> Optional["Period"]:
        max_start, min_end = max(self.start, other.start), min(self.end, other.end)

        return Period(start=max_start, end=min_end) if max_start <= min_end else None

    def __repr__(self) -> str:
        return f"({self.start.strftime('%d.%m.%Y')}, {self.end.strftime('%d.%m.%Y')})"


@dataclass(frozen=True, eq=True)
class Day(Period):
    def __init__(self, value: date) -> None:
        super().__init__(start=value, end=value)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Day):
            raise DomainException(f"Ожидался справа операнд {Day.__name__}, но был получен {other.__class__.__name__}")

        return self.start > other.start

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Day):
            raise DomainException(f"Ожидался справа операнд {Day.__name__}, но был получен {other.__class__.__name__}")

        return self.start < other.start

    def __le__(self, other: object) -> bool:
        return not self.__gt__(other)

    def __ge__(self, other: object) -> bool:
        return not self.__lt__(other)

    @classmethod
    def today(cls) -> "Day":
        return cls(now().date())


class Timeline(Iterable[Period]):
    def __init__(self) -> None:
        self._timeline: list[Period] = []

    def insert(self, period: Period) -> None:
        if not self._timeline:
            self._timeline = [period]
            return

        result = []
        intervals = sorted(self._timeline + [period], key=lambda x: x.start)
        accumulated = intervals[0]

        for i in range(1, len(intervals)):
            current = intervals[i]

            if current.start <= accumulated.end + timedelta(days=1):
                accumulated = Period(start=accumulated.start, end=max(current.end, accumulated.end))
                continue

            result.append(accumulated)
            accumulated = current

        result.append(accumulated)

        self._timeline = result

    def exclude(self, period: Period) -> None:
        start = end = self._find_intersection_index(period)

        periods: deque[Period] = deque()

        while end < len(self._timeline):
            current = self._timeline[end]
            intersection = period.intersects(current)

            if not intersection:
                break

            if intersection.start > current.start:
                periods.append(Period(start=current.start, end=intersection.start - timedelta(days=1)))

            if intersection.end < current.end:
                periods.append(Period(start=intersection.end + timedelta(days=1), end=current.end))

            end += 1

        self._timeline = self._timeline[:start] + list(periods) + self._timeline[end:]

    def __iter__(self) -> Iterator[Period]:
        yield from self._timeline

    def __contains__(self, item: object) -> bool:
        if not isinstance(item, Day):
            raise DomainException(f"Ожидался тип {Day.__name__}, но был получен {item.__class__.__name__}")

        idx = self._find_intersection_index(item)

        return idx < len(self._timeline) and bool(item.intersects(self._timeline[idx]))

    def _find_intersection_index(self, period: Period) -> int:
        left, right = 0, len(self._timeline)

        while left < right:
            mid = (left + right) // 2
            left, right = (mid + 1, right) if period.start > self._timeline[mid].end else (left, mid)

        return left

    @classmethod
    def from_iterable(cls, periods: Iterable[Period]) -> "Timeline":
        instance = cls()

        for period in periods:
            instance.insert(period)

        return instance