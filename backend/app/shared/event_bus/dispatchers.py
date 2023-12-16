from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4

from app.shared.event import Event
from app.shared.event_bus.outbox import Outbox, Status
from app.shared.event_bus.repositories import IOutboxRepository


class IEventDispatcher(ABC):
    @abstractmethod
    async def dispatch(self, event: Event) -> None:
        raise NotImplementedError


class OutboxEventDispatcher(IEventDispatcher):
    def __init__(self, outboxes: IOutboxRepository) -> None:
        self._outboxes = outboxes

    async def dispatch(self, event: Event) -> None:
        outbox = Outbox(
            id=uuid4(),
            event=event.name,
            data=event.to_json(),
            status=Status.UNDELIVERED,
            send_attempts=0,
            last_send_attempt_on=None,
            last_send_error=None,
            created_at=datetime.now(),
        )
        await self._outboxes.save(outbox)
