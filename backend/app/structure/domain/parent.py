from dataclasses import dataclass

from app.shared.domain.user import UserID


@dataclass(frozen=True, eq=True)
class ParentID(UserID):
    pass


@dataclass
class Parent:
    id: ParentID
