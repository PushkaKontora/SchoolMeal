from loguru import logger

from src.data.menu import generate_foods, generate_menus
from src.data.schools import generate_school
from src.data.users import generate_users
from src.db import Connection, DatabaseSettings
from src.schemas import Data, NutritionInitializer, SchemaInitializer, UserManagementInitializer


def main() -> None:
    school = generate_school()
    foods = generate_foods()
    menus = generate_menus(foods)
    users = generate_users()
    data = Data(school=school, menus=menus, foods=foods, users=users)
    logger.success("Сгенерированы данные")

    connection = Connection(settings=DatabaseSettings())

    initializers: list[type[SchemaInitializer]] = [
        UserManagementInitializer,
        NutritionInitializer,
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
