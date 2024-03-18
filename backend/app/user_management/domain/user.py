from dataclasses import dataclass
from enum import IntEnum, unique

from app.shared.domain.personal_info import FullName
from app.shared.domain.user import UserID
from app.user_management.domain.credentials import HashedPassword, Login


@unique
class Role(IntEnum):
    PARENT = 0
    TEACHER = 1
    STAFF = 2
    ADMIN = 3


@dataclass
class User:
    id: UserID
    login: Login
    password: HashedPassword
    role: Role
    name: FullName
