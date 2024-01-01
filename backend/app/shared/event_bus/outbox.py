from datetime import datetime
from enum import IntEnum, unique
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.event_bus.types import JSON


class OutboxAlreadyProcessed(Exception):
    pass


@unique
class Status(IntEnum):
    UNDELIVERED = 0
    DELIVERED = 1
    DISCARDED = 2
    SKIPPED = 3


@dataclass
class Outbox:
    id: UUID
    data: JSON
    event: str
    status: Status
    send_attempts: int
    last_send_attempt_on: datetime | None
    last_send_error: str | None
    created_at: datetime

    def deliver(self) -> None:
        """
        :raise OutboxAlreadyProcessed: сообщение уже обработано
        """

        self._increase_sending_attempts()
        self.status = Status.DELIVERED

    def skip(self) -> None:
        """
        :raise OutboxAlreadyProcessed: сообщение уже обработано
        """

        self._increase_sending_attempts()
        self.status = Status.SKIPPED

    def fail(self, error: str) -> None:
        """
        :raise OutboxAlreadyProcessed: сообщение уже обработано
        """

        self._increase_sending_attempts()
        self.last_send_error = error

        if self.send_attempts > 3:
            self.status = Status.DISCARDED

    def _increase_sending_attempts(self) -> None:
        """
        :raise OutboxAlreadyProcessed: сообщение уже обработано
        """

        if self.status != Status.UNDELIVERED:
            raise OutboxAlreadyProcessed

        self.send_attempts += 1
