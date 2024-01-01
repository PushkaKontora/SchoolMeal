from itertools import chain

import bcrypt
from pydantic.dataclasses import dataclass

from app.shared.domain import ValueObject


LATIN = "abcdefghijklmnopqrstuvwxyz"
CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
ASCII_ALPHABET: set[str] = set(chain.from_iterable([char.lower(), char.upper()] for char in LATIN + CYRILLIC))
SPECIAL_CHARACTERS = {
    "~",
    "!",
    "?",
    "@",
    "#",
    "$",
    "%",
    "^",
    "&",
    "*",
    "_",
    "-",
    "+",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ">",
    "<",
    "/",
    "\\",
    "|",
    '"',
    "'",
    ".",
    ",",
    ":",
    ";",
}


MIN_LENGTH = 8
MAX_LENGTH = 128


class InvalidPasswordFormat(Exception):
    pass


class PasswordIsEmpty(InvalidPasswordFormat):
    pass


class PasswordIsShort(InvalidPasswordFormat):
    pass


class PasswordIsLong(InvalidPasswordFormat):
    pass


class PasswordDoesntContainUpperLetter(InvalidPasswordFormat):
    pass


class PasswordDoesntContainLowerLetter(InvalidPasswordFormat):
    pass


class PasswordMustContainOnlyASCIILetter(InvalidPasswordFormat):
    pass


class PasswordDoesntContainDigit(InvalidPasswordFormat):
    pass


class PasswordMustNotContainSpaces(InvalidPasswordFormat):
    pass


class PasswordContainsUnavailableSpecialCharacter(InvalidPasswordFormat):
    pass


@dataclass(eq=True, frozen=True)
class Password(ValueObject):
    value: str

    def __post_init_post_parse__(self) -> None:
        if not self.value:
            raise PasswordIsEmpty

    def hash(self) -> "HashedPassword":
        return HashedPassword(bcrypt.hashpw(self.value.encode(), bcrypt.gensalt()))

    def as_strict(self) -> "StrictPassword":
        return StrictPassword(self.value)


@dataclass(eq=True, frozen=True)
class StrictPassword(Password):
    def __post_init_post_parse__(self) -> None:
        super().__post_init_post_parse__()

        if len(self.value) < MIN_LENGTH:
            raise PasswordIsShort

        if len(self.value) > MAX_LENGTH:
            raise PasswordIsLong

        if not any(char.isupper() for char in self.value):
            raise PasswordDoesntContainUpperLetter

        if not any(char.islower() for char in self.value):
            raise PasswordDoesntContainLowerLetter

        if not all(char in ASCII_ALPHABET for char in self.value if char.isalpha()):
            raise PasswordMustContainOnlyASCIILetter

        if not any(char.isdigit() for char in self.value):
            raise PasswordDoesntContainDigit

        if any(char.isspace() for char in self.value):
            raise PasswordMustNotContainSpaces

        if not all(char in SPECIAL_CHARACTERS for char in self.value if not char.isalnum()):
            raise PasswordContainsUnavailableSpecialCharacter


@dataclass(eq=True, frozen=True)
class HashedPassword(ValueObject):
    value: bytes

    def verify(self, password: Password) -> bool:
        return bcrypt.checkpw(password.value.encode(), self.value)
