from decimal import Decimal

from pydantic.dataclasses import dataclass

from app.shared.domain.abc import ValueObject


Number = Decimal | int | float


@dataclass(frozen=True, eq=True)
class Money(ValueObject):
    value: Decimal

    def __init__(self, value: Number) -> None:
        object.__setattr__(self, "value", Decimal(str(value)))

    def __post_init_post_parse__(self) -> None:
        if self.value < 0:
            raise ValueError("Отрицательное значение денег")

    def __add__(self, other: "Money") -> "Money":
        if not isinstance(other, Money):
            raise ValueError("Можно прибавлять только деньги с деньгами")

        return Money(self.value + other.value)

    def __mul__(self, other: int | float) -> "Money":
        if not isinstance(other, int | float):
            raise ValueError("Деньги можно увеличивать в целое или дробное число раз")

        return Money(self.value * Decimal(other))

    def __str__(self) -> str:
        return str(self.value)
