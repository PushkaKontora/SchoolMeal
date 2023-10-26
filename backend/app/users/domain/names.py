import re
from abc import ABC

from pydantic.dataclasses import dataclass

from app.common.domain.errors import DomainError


class InvalidFirstNameError(DomainError):
    pass


class InvalidLastNameError(DomainError):
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
            raise InvalidFirstNameError("Имя должно содержать только кириллицу") from error


@dataclass(eq=True, frozen=True)
class LastName(Name):
    def __post_init_post_parse__(self) -> None:
        try:
            super().__post_init_post_parse__()
        except ValueError as error:
            raise InvalidLastNameError("Фамилия должна содержать только кириллицу") from error
