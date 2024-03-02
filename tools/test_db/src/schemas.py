from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.data.menu import Food, Menu
from src.data.schools import School
from src.db import Array, Database, Date, Integer, Null, String


class Data(BaseModel):
    school: School
    menus: list[Menu]
    foods: list[Food]


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
        for table in ["school", "school_class", "teacher", "parent", "pupil", "request"]:
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

        self._database.insert(
            schema=self.schema,
            table="teacher",
            data={
                "id": String(school.teacher.id),
                "last_name": String(school.teacher.last_name),
                "first_name": String(school.teacher.first_name),
                "patronymic": String(school.teacher.patronymic),
            },
        )

        self._database.insert(
            schema=self.schema,
            table="parent",
            data={
                "id": String(school.parent.id),
                "last_name": String(school.parent.last_name),
                "first_name": String(school.parent.first_name),
                "patronymic": Null(),
                "email": String(school.parent.email),
                "phone": String(school.parent.phone),
                "children": Array(tuple()),
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
                        "cancellation": Array(tuple()),
                    },
                )
