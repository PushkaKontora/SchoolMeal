from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, eq=True)
class UserID:
    value: UUID

    @classmethod
    def generate(cls) -> "UserID":
        return cls(uuid4())
