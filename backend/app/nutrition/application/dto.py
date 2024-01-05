from datetime import date

from app.nutrition.domain.periods import CancellationPeriod
from app.shared.fastapi.schemas import FrontendModel


class CancellationPeriodOut(FrontendModel):
    starts_at: date
    ends_at: date
    reasons: list[str]

    @classmethod
    def from_model(cls, period: CancellationPeriod) -> "CancellationPeriodOut":
        return cls(
            starts_at=period.starts_at,
            ends_at=period.ends_at,
            reasons=[reason.value for reason in period.reasons],
        )
