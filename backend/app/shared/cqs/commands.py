from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class Command(BaseModel, ABC):
    pass


TCommand = TypeVar("TCommand", bound=Command)
TResult = TypeVar("TResult")


class ICommandHandler(Generic[TCommand, TResult], ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> TResult:
        raise NotImplementedError
