from datetime import date

from app.nutrition.domain.cancellation import CancellationPeriod
from app.shared.fastapi.schemas import FrontendModel


class CancellationPeriodOut(FrontendModel):
    starts_at: date
    ends_at: date
    reasons: list[str]

    @classmethod
    def from_model(cls, period: CancellationPeriod) -> "CancellationPeriodOut":
        return cls(
            starts_at=period.start,
            ends_at=period.end,
            reasons=[reason.value for reason in period.reasons],
        )
