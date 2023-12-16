from abc import ABC, abstractmethod

from app.shared.event_bus.outbox import Outbox, Status


class IOutboxRepository(ABC):
    @abstractmethod
    async def save(self, outbox: Outbox) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, outbox: Outbox) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_first_with(self, status: Status) -> Outbox | None:
        raise NotImplementedError
