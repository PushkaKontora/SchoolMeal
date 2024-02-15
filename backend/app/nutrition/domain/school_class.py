from dataclasses import dataclass
from uuid import UUID, uuid4

from app.nutrition.domain.mealtime import Mealtime


@dataclass(frozen=True)
class ClassID:
    value: UUID

    @classmethod
    def generate(cls) -> "ClassID":
        return cls(uuid4())


@dataclass
class SchoolClass:
    id: ClassID
    mealtimes: set[Mealtime]
