from enum import Enum, unique

from app.nutrition.domain.mealtime import Mealtime
from app.nutrition.domain.pupil import NutritionStatus
from app.nutrition.domain.school_class import Number


@unique
class SchoolClassTypeDTO(Enum):
    PRIMARY = "primary"
    HIGH = "high"

    def to_model_range(self) -> tuple[Number, Number]:
        return {
            SchoolClassTypeDTO.PRIMARY: (Number(1), Number(4)),
            SchoolClassTypeDTO.HIGH: (Number(5), Number(11)),
        }[self]


@unique
class MealtimeDTO(Enum):
    BREAKFAST = "breakfast"
    DINNER = "dinner"
    SNACKS = "snacks"

    def to_model(self) -> Mealtime:
        return {
            MealtimeDTO.BREAKFAST: Mealtime.BREAKFAST,
            MealtimeDTO.DINNER: Mealtime.DINNER,
            MealtimeDTO.SNACKS: Mealtime.SNACKS,
        }[self]

    @classmethod
    def from_model(cls, mealtime: Mealtime) -> "MealtimeDTO":
        return {
            Mealtime.BREAKFAST: cls.BREAKFAST,
            Mealtime.DINNER: cls.DINNER,
            Mealtime.SNACKS: cls.SNACKS,
        }[mealtime]


@unique
class NutritionStatusDTO(str, Enum):
    PAID = "paid"
    PREFERENTIAL = "preferential"

    @classmethod
    def from_model(cls, status: NutritionStatus) -> "NutritionStatusDTO":
        return {
            NutritionStatus.PAID: cls.PAID,
            NutritionStatus.PREFERENTIAL: cls.PREFERENTIAL,
        }[status]
