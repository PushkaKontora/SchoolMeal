from loguru import logger

from src.data.menu import generate_foods, generate_menus
from src.data.schools import generate_schools
from src.db import Connection, DatabaseSettings
from src.schemas import Data, FeedbacksSchemaInitializer, NutritionSchemaInitializer, SchemaInitializer


def main() -> None:
    schools = generate_schools()
    foods = generate_foods()
    menus = generate_menus(foods)
    data = Data(schools=schools, menus=menus, foods=foods)
    logger.success("Сгенерированы данные")

    connection = Connection(settings=DatabaseSettings())

    initializers: list[type[SchemaInitializer]] = [
        FeedbacksSchemaInitializer,
        NutritionSchemaInitializer,
    ]

    with connection as database:
        for initializer_cls in initializers:
            initializer = initializer_cls(database)

            initializer.clear()
            initializer.push(data)
            logger.success(f"Проинициализирована схема {initializer.schema}")

    logger.success("Инициализация завершена")


if __name__ == "__main__":
    main()
