from enum import IntEnum, unique


@unique
class Mealtime(IntEnum):
    BREAKFAST = 0
    DINNER = 10
    SNACKS = 20
