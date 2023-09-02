import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
from ipaddress import IPv4Address
from typing import Any, NamedTuple, TypeVar
from uuid import UUID, uuid4

import bcrypt
import jwt
from pydantic import Field
from pydantic.dataclasses import dataclass

from app import config
from app.common.domain.model import now
from app.user.domain.errors import (
    EmptyFirstNameError,
    EmptyLastNameError,
    EmptyLoginError,
    EmptyPasswordError,
    InvalidEmailFormatError,
    InvalidPhoneFormatError,
    InvalidPhotoURLError,
    InvalidTokenError,
    NotVerifiedPasswordError,
    RevokedTokenError,
    TokenExpirationError,
)


@dataclass
class UserID:
    value: UUID


class UserRole(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    MEAL_ORGANIZER = "meal_organizer"
    CANTEEN_STAFF = "canteen_staff"


@dataclass
class Login:
    value: str

    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise EmptyLoginError

        self.value = value


@dataclass
class Password:
    value: str

    def __init__(self, value: str) -> None:
        if len(value) == 0:
            raise EmptyPasswordError

        self.value = value

    def hash(self) -> "HashedPassword":
        return HashedPassword(value=bcrypt.hashpw(self.value.encode(), bcrypt.gensalt()))

    def verify(self, hashed_password: "HashedPassword") -> bool:
        return bcrypt.checkpw(self.value.encode(), hashed_password.value)


@dataclass
class HashedPassword:
    value: bytes


@dataclass
class Phone:
    value: str

    def __init__(self, value: str) -> None:
        if not re.match(r"^\+[1-9][0-9]{11}$", value):
            raise InvalidPhoneFormatError

        self.value = value


@dataclass
class FirstName:
    value: str

    def __init__(self, value: str):
        if len(value) == 0:
            raise EmptyFirstNameError

        self.value = value


@dataclass
class LastName:
    value: str

    def __init__(self, value: str):
        if len(value) == 0:
            raise EmptyLastNameError

        self.value = value


@dataclass
class Email:
    value: str

    def __init__(self, value: str) -> None:
        if not ("@" in value and re.match(r"^\S+@\S+\.\S+$", value)):
            raise InvalidEmailFormatError

        self.value = value


@dataclass
class Photo:
    url: str

    def __init__(self, url: str) -> None:
        if not re.match(
            "^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",
            url,
        ):
            raise InvalidPhotoURLError

        self.url = url


TToken = TypeVar("TToken", bound="Token")


@dataclass
class Token(ABC):
    user_id: UserID
    user_role: UserRole
    created_at: datetime = Field(default_factory=now)

    @property
    def is_expired(self) -> bool:
        return self.expires_in >= now().timestamp()

    @property
    def expires_in(self) -> int:
        dt = self.created_at + self._get_exp()

        return int(dt.timestamp())

    def to_dict(self) -> dict[str, Any]:
        return {
            "token": self._get_name(),
            "user_id": self.user_id,
            "user_role": self.user_role.value,
            "expires_in": self.expires_in,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return jwt.encode(self.to_dict(), config.jwt.secret, config.jwt.algorithm)

    @classmethod
    @abstractmethod
    def _get_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _get_exp(cls) -> timedelta:
        raise NotImplementedError

    @classmethod
    def decode(cls: type[TToken], value: str) -> TToken:
        """
        :raise InvalidTokenError: строка не является токеном
        """

        try:
            payload = jwt.decode(
                value,
                config.jwt.secret,
                [config.jwt.algorithm],
            )
        except jwt.InvalidTokenError as error:
            raise InvalidTokenError from error

        if payload["token"] != cls._get_name():
            raise InvalidTokenError

        return cls(
            user_id=UserID(payload["user_id"]),
            user_role=UserRole(payload["user_role"]),
            created_at=payload["created_at"],
        )


class AccessToken(Token):
    @classmethod
    def _get_name(cls) -> str:
        return "access"

    @classmethod
    def _get_exp(cls) -> timedelta:
        return config.jwt.access_lifetime


class RefreshToken(Token):
    @classmethod
    def _get_name(cls) -> str:
        return "refresh"

    @classmethod
    def _get_exp(cls) -> timedelta:
        return config.jwt.refresh_lifetime


class Tokens(NamedTuple):
    access: AccessToken
    refresh: RefreshToken


@dataclass
class User:
    id: UserID
    role: UserRole
    login: Login
    hashed_password: HashedPassword

    first_name: FirstName
    last_name: LastName
    email: Email | None
    phone: Phone | None
    photo: Photo | None

    authenticated_ips: dict[IPv4Address, RefreshToken] = Field(default_factory=dict)

    def authenticate(self, password: Password, ip: IPv4Address) -> Tokens:
        """
        :raise NotVerifiedPasswordError: пароль не совпадает с действительным
        """

        if not password.verify(self.hashed_password):
            raise NotVerifiedPasswordError

        return self._reissue_tokens(ip)

    def reissue_tokens_for(self, refresh_token: RefreshToken, ip: IPv4Address) -> Tokens:
        """
        :raise RevokedTokenError: токен уже был отозван
        :raise TokenExpirationError: токен протух
        """

        if ip in self.authenticated_ips and refresh_token != self.authenticated_ips[ip]:
            self.authenticated_ips.clear()
            raise RevokedTokenError

        if refresh_token.is_expired:
            raise TokenExpirationError

        return self._reissue_tokens(ip)

    def _reissue_tokens(self, ip: IPv4Address) -> Tokens:
        access_token, refresh_token = AccessToken(self.id, self.role), RefreshToken(self.id, self.role)
        self.authenticated_ips[ip] = refresh_token

        return Tokens(access_token, refresh_token)

    @staticmethod
    def create_parent(
        phone: Phone,
        password: HashedPassword,
        first_name: FirstName,
        last_name: LastName,
        email: Email,
    ) -> "User":
        return User(
            id=UserID(uuid4()),
            login=Login(phone.value),
            hashed_password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            role=UserRole.PARENT,
            photo=None,
        )
