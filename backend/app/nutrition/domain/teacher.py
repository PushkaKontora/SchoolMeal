from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, eq=True)
class TeacherID:
    value: UUID


@dataclass
class Teacher:
    id: TeacherID
