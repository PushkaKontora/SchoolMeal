from abc import ABC, abstractmethod

from src.db import Bool, Database, Date, Null, String, Integer
from src.schools import School


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
    def push(self, schools: list[School]) -> None:
        raise NotImplementedError


class FeedbacksSchemaInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "feedbacks"

    def clear(self) -> None:
        for table in ["canteen"]:
            self._database.truncate(self.schema, table)

    def push(self, schools: list[School]) -> None:
        for school in schools:
            self._database.insert(self.schema, "canteen", data={"id": String(school.id)})


class NutritionSchemaInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "nutrition"

    def clear(self) -> None:
        for table in ["pupil"]:
            self._database.truncate(self.schema, table)

    def push(self, schools: list[School]) -> None:
        for school in schools:
            self._database.insert(
                self.schema,
                "school",
                data={
                    "id": String(school.id),
                    "name": String(school.name),
                }
            )

            for school_class in school.school_classes:
                self._database.insert(
                    self.schema,
                    "school_class",
                    data={
                        "id": String(school_class.id),
                        "school_id": String(school.id),
                        "number": Integer(school_class.number),
                        "literal": String(school_class.literal),
                    }
                )

                for pupil in school_class.pupils:
                    meal_plan, certificate = pupil.meal_plan, pupil.preferential_certificate

                    self._database.insert(
                        self.schema,
                        "pupil",
                        data={
                            "id": String(pupil.id),
                            "last_name": String(pupil.last_name),
                            "first_name": String(pupil.first_name),
                            "patronymic": String(pupil.patronymic) if pupil.patronymic else Null(),
                            "has_breakfast": Bool(meal_plan.has_breakfast),
                            "has_dinner": Bool(meal_plan.has_dinner),
                            "has_snacks": Bool(meal_plan.has_snacks),
                            "preferential_certificate_ends_at": Date(certificate.ends_at) if certificate else Null(),
                            "school_class_id": String(school_class.id),
                        },
                    )
