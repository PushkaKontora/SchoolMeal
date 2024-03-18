from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class ParentID:
    value: UUID


@dataclass
class Parent:
    id: ParentID
