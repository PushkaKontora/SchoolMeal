from loguru import logger

from src.db import Connection, DatabaseSettings
from src.schemas import (
    ChildrenSchemaInitializer,
    FeedbacksSchemaInitializer,
    NutritionSchemaInitializer,
    SchemaInitializer,
)
from src.schools import generate_schools


def main() -> None:
    schools = generate_schools()
    logger.success("Сгенерированы данные")

    connection = Connection(settings=DatabaseSettings())

    initializers: list[type[SchemaInitializer]] = [
        ChildrenSchemaInitializer,
        FeedbacksSchemaInitializer,
        NutritionSchemaInitializer,
    ]

    with connection as database:
        for initializer_cls in initializers:
            initializer = initializer_cls(database)

            initializer.clear()
            initializer.push(schools)
            logger.success(f"Проинициализирована схема {initializer.schema}")

    logger.success("Инициализация завершена")


if __name__ == "__main__":
    main()
