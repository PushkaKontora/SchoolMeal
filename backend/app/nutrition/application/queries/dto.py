from enum import Enum

from app.nutrition.domain.pupil import NutritionStatus


class MealStatus(str, Enum):
    PREFERENTIAL = "Питается льготно"
    PAID = "Питается платно"
    NONE = "Не питается"

    @classmethod
    def from_model(cls, status: NutritionStatus) -> "MealStatus":
        mapper = {
            NutritionStatus.PREFERENTIAL: cls.PREFERENTIAL,
            NutritionStatus.PAID: cls.PAID,
            NutritionStatus.NONE: cls.NONE,
        }
        return mapper[status]
