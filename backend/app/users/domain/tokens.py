from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import TypeVar
from uuid import UUID

import jwt
from pydantic import ValidationError
from pydantic.dataclasses import dataclass

from app.common.domain.errors import DomainError


class InvalidTokenError(DomainError):
    pass


class InvalidSignatureError(InvalidTokenError):
    pass


class ExpirationSignatureError(InvalidTokenError):
    pass


T = TypeVar("T", bound="Token", covariant=True)


@dataclass(eq=True, frozen=True)
class Token(ABC):
    jti: UUID
    user_id: UUID
    device_id: UUID
    iat: datetime

    _ALGORITHM = "HS256"

    @property
    def exp(self) -> datetime:
        return self.iat + self._lifetime()

    def encode(self, secret: str) -> str:
        payload = {
            "jti": str(self.jti),
            "token": self._token_name(),
            "user_id": str(self.user_id),
            "device_id": str(self.device_id),
            "iat": self.iat.timestamp(),
            "exp": self.exp.timestamp(),
        }

        return jwt.encode(payload, key=secret, algorithm=self._ALGORITHM)

    @classmethod
    def decode(cls: type[T], token: str, secret: str) -> T:
        """
        :raise InvalidSignatureError: токен повреждён
        :raise ExpirationSignatureError: токен протух
        """

        try:
            payload = jwt.decode(
                token,
                key=secret,
                algorithms=[cls._ALGORITHM],
                options={"require": ["token", "jti", "user_id", "device_id", "iat", "exp"]},
            )

            if payload["token"] != cls._token_name():
                raise AssertionError

            return cls(
                jti=payload["jti"],
                user_id=payload["user_id"],
                device_id=payload["device_id"],
                iat=payload["iat"],
            )

        except jwt.ExpiredSignatureError as error:
            raise ExpirationSignatureError("Токен протух") from error

        except (jwt.InvalidTokenError, ValidationError, AssertionError) as error:
            raise InvalidSignatureError("Токен повреждён") from error

    @classmethod
    @abstractmethod
    def _token_name(cls) -> str:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def _lifetime(cls) -> timedelta:
        raise NotImplementedError


@dataclass(eq=True, frozen=True)
class AccessToken(Token):
    @classmethod
    def _token_name(cls) -> str:
        return "access"

    @classmethod
    def _lifetime(cls) -> timedelta:
        return timedelta(minutes=15)


@dataclass(eq=True, frozen=True)
class RefreshToken(Token):
    @classmethod
    def _token_name(cls) -> str:
        return "refresh"

    @classmethod
    def _lifetime(cls) -> timedelta:
        return timedelta(days=10)
