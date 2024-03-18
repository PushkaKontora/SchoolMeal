from enum import IntEnum
from uuid import UUID

import bcrypt
from pydantic import BaseModel


class Role(IntEnum):
    PARENT = 0
    TEACHER = 1
    STAFF = 2
    ADMIN = 3


class User(BaseModel):
    id: UUID
    login: str
    password: bytes
    role: Role
    last_name: str
    first_name: str
    patronymic: str | None


def generate_users() -> list[User]:
    password = bcrypt.hashpw(b"P@ssw0rd1234", salt=bcrypt.gensalt())

    parent = User(
        id=UUID("844c4372-52eb-4452-b314-728583ee5fbf"),
        role=Role.PARENT,
        login="8005553535",
        password=password,
        last_name="Кузьмин",
        first_name="Кузьмич",
        patronymic=None,
    )
    teacher = User(
        id=UUID("a5958f26-02f6-4e5f-b0f2-c26f847aa2f6"),
        role=Role.TEACHER,
        login="teacher",
        password=password,
        last_name="Лыкова",
        first_name="Агафья",
        patronymic="Андреевна",
    )
    staff = User(
        id=UUID("e0185f36-8f86-45e0-a218-a168270da3c1"),
        role=Role.STAFF,
        login="staff",
        password=password,
        last_name="Самкова",
        first_name="Елена",
        patronymic="Давыдова",
    )
    admin = User(
        id=UUID("4e4d3460-04c2-4813-8c9a-7218dc6419fe"),
        role=Role.ADMIN,
        login="admin",
        password=password,
        last_name="Перова",
        first_name="Зинаида",
        patronymic="Андреевна",
    )

    return [parent, teacher, staff, admin]
