from dataclasses import dataclass
from enum import Enum


class MealStatus(str, Enum):
    PREFERENTIAL = "preferential"
    PAID = "paid"
    NONE = "none"


@dataclass(eq=True, frozen=True)
class MealPlan:
    status: MealStatus
