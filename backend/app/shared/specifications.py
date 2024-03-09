from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class Specification(Generic[T], ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: T) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Specification[T]") -> "_AndSpecification[T]":
        return _AndSpecification(self, other)

    def __or__(self, other: "Specification[T]") -> "_OrSpecification[T]":
        return _OrSpecification(self, other)

    def __invert__(self) -> "_NotSpecification[T]":
        return _NotSpecification(self)


class TrueSpecification(Specification[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        return True


class FalseSpecification(Specification[T]):
    def is_satisfied_by(self, candidate: T) -> bool:
        return False


class _AndSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) and self._right.is_satisfied_by(candidate)


class _OrSpecification(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, candidate: T) -> bool:
        return self._left.is_satisfied_by(candidate) or self._right.is_satisfied_by(candidate)


class _NotSpecification(Specification[T]):
    def __init__(self, spec: Specification[T]) -> None:
        self._spec = spec

    def is_satisfied_by(self, candidate: T) -> bool:
        return not self._spec.is_satisfied_by(candidate)
