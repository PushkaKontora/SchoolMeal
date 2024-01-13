import random
from datetime import date, datetime, timedelta
from uuid import uuid4

from pydantic import BaseModel


class Food(BaseModel):
    id: str
    name: str
    description: str
    calories: int
    proteins: int
    fats: int
    carbohydrates: int
    weight: int
    price: int
    photo: str


class Menu(BaseModel):
    id: str
    on_date: date
    breakfast: list[Food]
    class_type: int
    dinner: list[Food]
    snacks: list[Food]


def generate_menus(foods: list[Food]) -> list[Menu]:
    now, half_year = datetime.now().date(), 365 // 2

    menus: list[Menu] = []

    for class_type in range(0, 2):
        for delta in range(-half_year, half_year + 1):
            menus.append(
                Menu(
                    id=str(uuid4()),
                    on_date=now + timedelta(days=delta),
                    class_type=class_type,
                    breakfast=random.sample(foods, k=random.randint(1, 2)),
                    dinner=random.sample(foods, k=random.randint(1, 5)),
                    snacks=random.sample(foods, k=random.randint(1, 2)),
                )
            )

    return menus


def generate_foods() -> list[Food]:
    foods = [
        ["Каша рисовая c маслом", "2.png"],
        ["Яблоко", "5.png"],
        ["Кисель с сухофруктами", "10.png"],
        ["Суп борщ с курицей", "7.png"],
        ["Суп борщ с курицей", "7.png"],
        ["Каша гречневая", "4.png"],
        ["Котлета рыбная", "11.png"],
        ["Компот из сухофруктов", "3.png"],
        ["Хлеб витаминный", "9.png"],
        ["Йогурт натуральный", "6.png"],
        ["Шаньга с картофелем", "1.png"],
    ]

    return [
        Food(
            id=str(uuid4()),
            name=name,
            description="",
            calories=random.randint(10, 100),
            proteins=random.randint(10, 100),
            fats=random.randint(10, 100),
            carbohydrates=random.randint(10, 100),
            weight=random.randint(20, 300),
            price=random.randint(10, 100),
            photo=photo,
        )
        for name, photo in foods
    ]
