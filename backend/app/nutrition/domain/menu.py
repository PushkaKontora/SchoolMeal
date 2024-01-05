from datetime import date
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.nutrition.domain.school_class import SchoolClassType
from app.shared.domain.abc import Entity
from app.shared.domain.money import Money


@dataclass
class Food(Entity):
    id: UUID
    name: str
    description: str
    calories: Decimal
    proteins: Decimal
    fats: Decimal
    carbohydrates: Decimal
    price: Money
    photo: Path


@dataclass
class Menu(Entity):
    id: UUID
    school_class_type: SchoolClassType
    on_date: date
    breakfast_foods: list[Food]
    dinner_foods: list[Food]
    snacks_foods: list[Food]
