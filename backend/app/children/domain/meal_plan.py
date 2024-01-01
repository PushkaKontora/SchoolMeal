from enum import Enum

from pydantic.dataclasses import dataclass

from app.shared.domain import ValueObject


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


@dataclass(eq=True, frozen=True)
class MealPlan(ValueObject):
    status: MealStatus
