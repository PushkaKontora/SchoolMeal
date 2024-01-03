from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel


class Query(BaseModel, ABC):
    pass


TQuery = TypeVar("TQuery", bound=Query)
TResult = TypeVar("TResult")


class IQueryExecutor(Generic[TQuery, TResult], ABC):
    @abstractmethod
    async def execute(self, query: TQuery) -> TResult:
        raise NotImplementedError
