from dataclasses import dataclass

from app.shared.domain.user import UserID


@dataclass(frozen=True)
class NotFoundUser:
    id: UserID
