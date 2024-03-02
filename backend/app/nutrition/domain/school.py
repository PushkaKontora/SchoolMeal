from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class SchoolName:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Значение должно быть определено")


@dataclass
class School:
    name: SchoolName
