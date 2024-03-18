import re
from dataclasses import dataclass

from email_validator import EmailSyntaxError, validate_email


@dataclass(frozen=True, eq=True)
class Name:
    value: str

    _MAX_LENGTH = 64
    _REGEX = re.compile(r"[А-ЯЁ][а-яё]*")

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Значение должно быть определено")

        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышено максимальное количество символов - {self._MAX_LENGTH}")

        if not self._REGEX.fullmatch(self.value):
            raise ValueError(
                "Первая буква имени должна быть кириллицей в верхнем регистре, остальные - в нижнем регистре"
            )

    @classmethod
    def create(cls, value: str) -> "Name":
        return cls(value.capitalize())


@dataclass(frozen=True, eq=True)
class FullName:
    last: Name
    first: Name
    patronymic: Name | None

    @classmethod
    def create(cls, last: str, first: str, patronymic: str | None = None) -> "FullName":
        return cls(
            last=Name.create(last),
            first=Name.create(first),
            patronymic=Name.create(patronymic) if patronymic is not None else None,
        )


@dataclass(frozen=True, eq=True)
class Email:
    value: str

    _MAX_LENGTH = 64

    def __post_init__(self) -> None:
        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Превышено максимальное количество символов - {self._MAX_LENGTH}")

        try:
            validate_email(self.value, check_deliverability=False)
        except EmailSyntaxError as error:
            raise ValueError("Неверный формат почты") from error


@dataclass(frozen=True, eq=True)
class Phone:
    value: str

    _REGEX = re.compile(r"\d{10}")

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Значение должно быть определёно")

        if not self._REGEX.fullmatch(self.value):
            raise ValueError("Ожидалось 10 цифр")
