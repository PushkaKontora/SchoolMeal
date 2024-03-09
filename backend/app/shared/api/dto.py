from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar

from pydantic import BaseModel

from app.shared.specifications import Specification, TrueSpecification


T = TypeVar("T")


class Filters(Generic[T], BaseModel, ABC):
    def to_specification(self) -> Specification[T]:
        map_ = self._build_map()

        spec: Specification[T] = TrueSpecification[T]()

        for attr, value in self.dict().items():
            if value is None:
                continue

            spec &= map_[attr](value)

        return spec

    @abstractmethod
    def _build_map(self) -> dict[str, Callable[[Any], Specification[T]]]:
        raise NotImplementedError
