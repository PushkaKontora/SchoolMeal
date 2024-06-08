from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.data.menu import Food, Menu
from src.data.schools import School
from src.data.users import User
from src.db import Array, Database, Date, Integer, Null, String


class Data(BaseModel):
    school: School
    menus: list[Menu]
    foods: list[Food]
    users: list[User]


class SchemaInitializer(ABC):
    def __init__(self, database: Database) -> None:
        self._database = database

    @property
    @abstractmethod
    def schema(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def push(self, data: Data) -> None:
        raise NotImplementedError


class NutritionInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "nutrition"

    def clear(self) -> None:
        for table in ["school_class", "pupil", "declaration", "request", "school", "pupil_parent"]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        school = data.school

        self._database.insert(
            schema=self.schema,
            table="school",
            data={
                "id": Integer(1),
                "name": String(school.name),
            },
        )

        for school_class in data.school.school_classes:
            self._database.insert(
                schema=self.schema,
                table="school_class",
                data={
                    "id": String(school_class.id),
                    "teacher_id": String(school.teacher.id),
                    "number": Integer(school_class.number),
                    "literal": String(school_class.literal),
                    "mealtimes": Array(tuple(Integer(v) for v in school_class.mealtimes)),
                },
            )

            for pupil in school_class.pupils:
                self._database.insert(
                    schema=self.schema,
                    table="pupil",
                    data={
                        "id": String(pupil.id),
                        "class_id": String(school_class.id),
                        "last_name": String(pupil.last_name),
                        "first_name": String(pupil.first_name),
                        "patronymic": String(pupil.patronymic) if pupil.patronymic else Null(),
                        "mealtimes": Array(tuple(Integer(v) for v in pupil.mealtimes)),
                        "preferential_until": Date(pupil.preferential_until) if pupil.preferential_until else Null(),
                        "cancelled_periods": Array(tuple()),
                    },
                )

                self._database.insert(
                    schema=self.schema,
                    table="pupil_parent",
                    data={
                        "pupil_id": String(pupil.id),
                        "parent_id": String(data.school.parent.id),
                    },
                )


class UserManagementInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "user_management"

    def clear(self) -> None:
        for table in ["session", "user"]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        for user in data.users:
            self._database.insert(
                schema=self.schema,
                table="user",
                data={
                    "id": String(str(user.id)),
                    "login": String(user.login),
                    "password": String(user.password.decode()),
                    "role": Integer(user.role.value),
                    "last_name": String(user.last_name),
                    "first_name": String(user.first_name),
                    "patronymic": String(user.patronymic) if user.patronymic else Null(),
                },
            )
