from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, eq=True)
class ClassID:
    value: UUID

    @classmethod
    def generate(cls) -> "ClassID":
        return cls(uuid4())
