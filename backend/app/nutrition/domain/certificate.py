from datetime import date, datetime, timezone

from pydantic.dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class PreferentialCertificate:
    ends_at: date

    @property
    def is_expired(self) -> bool:
        return datetime.now(timezone.utc).date() > self.ends_at
