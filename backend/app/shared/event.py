from abc import ABC, abstractmethod

from app.shared.event_bus.types import JSON


class Event(ABC):
    @property
    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def to_json(self) -> JSON:
        raise NotImplementedError
