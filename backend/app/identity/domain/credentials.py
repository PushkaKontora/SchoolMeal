import re
import string
from dataclasses import dataclass

import bcrypt


_LETTERS = set(string.ascii_letters)
_SPECIAL = {
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


@dataclass(frozen=True, eq=True)
class Login:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Логин должен быть определён")


@dataclass(frozen=True)
class HashedPassword:
    value: bytes

    def verify(self, password: "Password") -> bool:
        return bcrypt.checkpw(password.value.encode(), self.value)


@dataclass(frozen=True, eq=True)
class Password:
    value: str

    _REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&-+=()!? \"]).{8,30}$")

    _MIN_LENGTH = 8
    _MAX_LENGTH = 30

    def __post_init__(self) -> None:
        if len(self.value) < self._MIN_LENGTH:
            raise ValueError("Пароль слишком короткий")

        if len(self.value) > self._MAX_LENGTH:
            raise ValueError("Пароль слишком длинный")

        if not all(char in _LETTERS for char in self.value if char.isalpha()):
            raise ValueError("Пароль может содержать только латинские буквы")

        if not any(char.isupper() for char in self.value):
            raise ValueError("Пароль не содержит заглавную букву")

        if not any(char.islower() for char in self.value):
            raise ValueError("Пароль не содержит строчную букву")

        if not any(char.isdigit() for char in self.value):
            raise ValueError("Пароль не содержит цифру")

        if any(char.isspace() for char in self.value):
            raise ValueError("Пароль не должен содержать пробелов")

        if not all(char in _SPECIAL for char in self.value if not char.isalnum()):
            raise ValueError("Пароль не содержит специальных символов")

    def hash(self) -> HashedPassword:
        return HashedPassword(bcrypt.hashpw(self.value.encode(), salt=bcrypt.gensalt()))
