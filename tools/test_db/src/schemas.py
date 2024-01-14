from abc import ABC, abstractmethod

from pydantic import BaseModel

from src.data.menu import Food, Menu
from src.data.schools import School
from src.db import Bool, Database, Date, Integer, Null, String


class Data(BaseModel):
    schools: list[School]
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


class FeedbacksSchemaInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "feedbacks"

    def clear(self) -> None:
        for table in ["canteen"]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        for school in data.schools:
            self._database.insert(self.schema, "canteen", data={"id": String(school.id)})


class NutritionSchemaInitializer(SchemaInitializer):
    @property
    def schema(self) -> str:
        return "nutrition"

    def clear(self) -> None:
        for table in [
            "school",
            "school_class",
            "pupil",
            "food",
            "menu",
            *[f"{mealtime}_food" for mealtime in ["breakfast", "dinner", "snacks"]],
        ]:
            self._database.truncate(self.schema, table)

    def push(self, data: Data) -> None:
        self._push_schools(data.schools)
        self._push_foods(data.foods)
        self._push_menus(data.menus)

    def _push_foods(self, foods: list[Food]) -> None:
        for food in foods:
            self._database.insert(
                self.schema,
                "food",
                data={
                    "id": String(food.id),
                    "name": String(food.name),
                    "description": String(food.description),
                    "calories": Integer(food.calories),
                    "proteins": Integer(food.proteins),
                    "fats": Integer(food.fats),
                    "carbohydrates": Integer(food.carbohydrates),
                    "price": Integer(food.price),
                    "photo": String(food.photo),
                    "weight": Integer(food.weight),
                },
            )

    def _push_menus(self, menus: list[Menu]) -> None:
        def __push_relative(menu_id: str, mealtime_: str, foods_: list[Food]) -> None:
            for food in foods_:
                self._database.insert(
                    self.schema,
                    f"{mealtime_}_food",
                    data={
                        "menu_id": String(menu_id),
                        "food_id": String(food.id),
                    },
                )

        for menu in menus:
            self._database.insert(
                self.schema,
                "menu",
                data={
                    "id": String(menu.id),
                    "school_class_type": Integer(menu.class_type),
                    "on_date": Date(menu.on_date),
                },
            )

            for mealtime, foods in [["breakfast", menu.breakfast], ["dinner", menu.dinner], ["snacks", menu.snacks]]:
                __push_relative(menu_id=menu.id, mealtime_=mealtime, foods_=foods)

    def _push_schools(self, schools: list[School]) -> None:
        for school in schools:
            self._database.insert(
                self.schema,
                "school",
                data={
                    "id": String(school.id),
                    "name": String(school.name),
                },
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
                    },
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
