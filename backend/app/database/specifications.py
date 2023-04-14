from abc import ABC, abstractmethod
from typing import TypeVar

from sqlalchemy import Select


TQuery = TypeVar("TQuery", bound=Select)


class Specification(ABC):
    @abstractmethod
    def to_query(self, query: TQuery) -> TQuery:
        raise NotImplementedError


class FilterSpecification(Specification, ABC):
    @abstractmethod
    def __and__(self, other: "FilterSpecification") -> "FilterSpecification":
        raise NotImplementedError

    @abstractmethod
    def __or__(self, other: "FilterSpecification") -> "FilterSpecification":
        raise NotImplementedError

    @abstractmethod
    def __invert__(self) -> "FilterSpecification":
        raise NotImplementedError
