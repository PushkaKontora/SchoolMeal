from dataclasses import dataclass

from app.shared.event_bus.repositories import IOutboxRepository
from app.shared.unit_of_work.abc import Context


@dataclass(frozen=True)
class OutboxContext(Context):
    outboxes: IOutboxRepository
