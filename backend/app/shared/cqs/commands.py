from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class Command(BaseModel, ABC):
    pass


TCommand = TypeVar("TCommand", bound=Command)


class ICommandHandler(Generic[TCommand], ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> None:
        raise NotImplementedError
