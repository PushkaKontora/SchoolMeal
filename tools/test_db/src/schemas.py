import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

from pydantic import BaseModel

from src.data.menu import Food, Menu
from src.data.schools import Pupil, School
from src.data.users import Role, User
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
        for table in ["school_class", "pupil", "declaration", "teacher", "parent", "request", "school", "pupil_parent"]:
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


class NotificationInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "notification"

    def clear(self) -> None:
        for table in ["notification", "user"]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        teacher = next(user for user in data.users if user.role is Role.TEACHER)
        school_class = data.school.school_classes[0]

        notifications: list[tuple[Pupil, str, str]] = [
            (school_class.pupils[0], "", "17.06.2024"),
            (school_class.pupils[1], "Поднялась температура, неделю на больничном", "17.06.2024 - 21.06.2024"),
            (
                school_class.pupils[2],
                "Пошёл гулять с друзьями, нашли какую-то странную собаку, собака покусала - лежим в больнице",
                "10.06.2024 - 21.06.2024",
            ),
            (school_class.pupils[3], "Уезжает на соревнования", "14.06.2024"),
            (school_class.pupils[4], "Уедем в другой город ко врачу", "20.06.2024"),
        ]

        for pupil, reason, period in notifications:
            self._database.insert(
                self.schema,
                table="notification",
                data={
                    "id": String(str(uuid.uuid4())),
                    "recipients": Array((String(str(teacher.id)),)),
                    "title": String(f"{pupil.first_name} {pupil.last_name}"),
                    "subtitle": String(f"не будет питаться {period}"),
                    "mark": String(f"{school_class.number}{school_class.literal}"),
                    "body": String(reason),
                    "created_at": Date(datetime.now(timezone.utc)),
                },
            )


class FeedbacksInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "feedbacks"

    def clear(self) -> None:
        for table in ["feedback"]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        pass
