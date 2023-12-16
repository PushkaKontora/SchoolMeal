from abc import ABC, abstractmethod
from types import TracebackType

from app.shared.event_bus.outbox import Outbox


class FailedSending(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class IEventSender(ABC):
    @abstractmethod
    async def send(self, outbox: Outbox) -> None:
        """
        :raise FailedSending: ошибка отправки сообщения
        """
        raise NotImplementedError


class ISenderConnection(ABC):
    @abstractmethod
    async def __aenter__(self) -> IEventSender:
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        raise NotImplementedError


class IBusConnector(ABC):
    @abstractmethod
    def sender(self) -> ISenderConnection:
        raise NotImplementedError
