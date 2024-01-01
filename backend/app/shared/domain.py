from abc import ABC
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    pass


@dataclass(frozen=True, eq=True)
class ValueObject(ABC):
    pass
