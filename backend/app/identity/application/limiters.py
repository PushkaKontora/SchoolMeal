from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address


class IBruteForceLimiter(ABC):
    @abstractmethod
    def is_ip_banned(self, ip: IPv4Address) -> bool:
        raise NotImplementedError

    @abstractmethod
    def increase_attempts(self, ip: IPv4Address) -> None:
        raise NotImplementedError

    @abstractmethod
    def reset(self, ip: IPv4Address) -> None:
        raise NotImplementedError


class BruteForceLimiter(IBruteForceLimiter):
    _MAX_ATTEMPTS = 5
    _BAN_PERIOD = timedelta(hours=5)

    def __init__(self) -> None:
        self._ips: defaultdict[IPv4Address, _Info] = defaultdict(lambda: _Info(attempts=0, banned_until=None))

    def is_ip_banned(self, ip: IPv4Address) -> bool:
        return self._ips[ip].banned_until and self._now() <= self._ips[ip].banned_until

    def increase_attempts(self, ip: IPv4Address) -> None:
        info = self._ips[ip]

        info.attempts += 1

        if info.attempts > self._MAX_ATTEMPTS and not info.banned_until:
            info.banned_until = self._now() + self._BAN_PERIOD

    def reset(self, ip: IPv4Address) -> None:
        self._ips[ip] = _Info(attempts=0, banned_until=None)

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)


@dataclass
class _Info:
    attempts: int
    banned_until: datetime | None
