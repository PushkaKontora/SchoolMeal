from datetime import date

from app.shared.fastapi.schemas import FrontendModel


class Mealtimes(FrontendModel):
    has_breakfast: bool
    has_dinner: bool
    has_snacks: bool


class CancellationPeriod(FrontendModel):
    starts_at: date
    ends_at: date
    reason: str | None
