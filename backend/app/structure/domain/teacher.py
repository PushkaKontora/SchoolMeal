from dataclasses import dataclass

from app.shared.domain.user import UserID


@dataclass(frozen=True, eq=True)
class TeacherID(UserID):
    pass


@dataclass
class Teacher:
    id: TeacherID
