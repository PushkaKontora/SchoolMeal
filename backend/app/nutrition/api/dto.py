from enum import Enum

from pydantic import BaseModel

from app.nutrition.domain.mealtime import Mealtime


class MealtimeDTO(str, Enum):
    BREAKFAST = "breakfast"
    DINNER = "dinner"
    SNACKS = "snacks"

    def to_model(self) -> Mealtime:
        return {
            self.BREAKFAST: Mealtime.BREAKFAST,
            self.DINNER: Mealtime.DINNER,
            self.SNACKS: Mealtime.SNACKS,
        }[self]


class ResumedPupilIn(BaseModel):
    id: str
    mealtimes: set[MealtimeDTO]

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ResumedPupilIn) and self.id == other.id
