import re
from abc import ABC

from pydantic.dataclasses import dataclass


class FirstNameContainsNotCyrillicCharacters(Exception):
    pass


class LastNameContainsNotCyrillicCharacters(Exception):
    pass


@dataclass(eq=True, frozen=True)
class Name(ABC):
    value: str

    def __post_init_post_parse__(self) -> None:
        if not re.match(r"^[а-яА-Я ]+$", self.value):
            raise ValueError


@dataclass(eq=True, frozen=True)
class FirstName(Name):
    def __post_init_post_parse__(self) -> None:
        try:
            super().__post_init_post_parse__()
        except ValueError as error:
            raise FirstNameContainsNotCyrillicCharacters from error


@dataclass(eq=True, frozen=True)
class LastName(Name):
    def __post_init_post_parse__(self) -> None:
        try:
            super().__post_init_post_parse__()
        except ValueError as error:
            raise LastNameContainsNotCyrillicCharacters from error
