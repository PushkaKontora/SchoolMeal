from datetime import datetime

from pydantic import AnyHttpUrl, EmailStr, Field

from app.users.db.user.model import Role
from app.utils.entity import DatetimeField, Entity


class RegistrationSchema(Entity):
    phone: str = Field(regex=r"^\+7[0-9]{10}$")
    password: str
    email: EmailStr | None
    last_name: str
    first_name: str


class ProfileOut(Entity):
    id: int
    last_name: str
    first_name: str
    login: str
    role: Role
    phone: str | None = Field(example="+78005553535")
    email: EmailStr | None
    photo_path: AnyHttpUrl | None
    created_at: datetime = DatetimeField()


class ContactOut(Entity):
    id: int
    last_name: str
    first_name: str
    phone: str
    email: str
