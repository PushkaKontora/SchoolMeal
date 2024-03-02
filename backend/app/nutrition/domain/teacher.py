from dataclasses import dataclass
from uuid import UUID, uuid4

from app.nutrition.domain.personal_info import FullName


@dataclass(frozen=True, eq=True)
class TeacherID:
    value: UUID

    @classmethod
    def generate(cls) -> "TeacherID":
        return cls(uuid4())


@dataclass
class Teacher:
    id: TeacherID
    name: FullName
