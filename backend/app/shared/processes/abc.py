from abc import ABC, abstractmethod


class Process(ABC):
    def __init__(self) -> None:
        self._name = self.__class__.__name__

    @abstractmethod
    def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        raise NotImplementedError
