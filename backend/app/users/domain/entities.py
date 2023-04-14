from datetime import datetime
from enum import Enum as BaseEnum

from app.entities import BaseEntity


class Role(BaseEnum):
    PARENT = "parent"
    TEACHER = "teacher"
    EMPLOYEE = "employee"
    ORGANIZER = "organizer"


class User(BaseEntity):
    id: int
    last_name: str
    first_name: str
    login: str
    role: Role
    phone: str | None
    email: str | None
    photo_path: str | None
    created_at: datetime
