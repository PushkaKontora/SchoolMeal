from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID, uuid4

from dateutil.relativedelta import relativedelta

from app.shared.domain.user import UserID


@dataclass(frozen=True, eq=True)
class NotificationID:
    value: UUID

    @classmethod
    def generate(cls) -> "NotificationID":
        return cls(uuid4())


@dataclass(frozen=True, eq=True)
class Title:
    value: str

    _MAX_LENGTH = 64

    def __post_init__(self) -> None:
        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышена максимальная длина заголовка уведомления - {self._MAX_LENGTH} символов")


@dataclass(frozen=True, eq=True)
class Subtitle:
    value: str

    _MAX_LENGTH = 64

    def __post_init__(self) -> None:
        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышена максимальная длина подзаголовка уведомления - {self._MAX_LENGTH} символов")


@dataclass(frozen=True, eq=True)
class Mark:
    value: str

    _MAX_LENGTH = 3

    def __post_init__(self) -> None:
        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышена максимальная длина марки уведомления - {self._MAX_LENGTH} символов")


@dataclass(frozen=True, eq=True)
class Body:
    value: str

    _MAX_LENGTH = 255

    def __post_init__(self) -> None:
        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышена максимальная длина тела уведомления - {self._MAX_LENGTH} символов")


@dataclass
class Notification:
    id: NotificationID
    recipients: set[UserID]
    title: Title
    subtitle: Subtitle
    mark: Mark
    body: Body
    created_at: datetime

    @property
    def is_old(self) -> bool:
        return datetime.now(timezone.utc) > self.created_at + relativedelta(months=2)
