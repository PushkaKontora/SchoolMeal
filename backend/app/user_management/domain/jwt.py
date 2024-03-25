from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address
from typing import Any, Optional
from uuid import UUID, uuid4

import jwt
from pydantic import BaseModel, ValidationError

from app.shared.domain.user import UserID
from app.user_management.domain.user import Role, User


class Payload(BaseModel):
    jti: UUID
    iat: float
    exp: float
    user_id: UUID
    role: Role
    last_name: str
    first_name: str
    patronymic: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "jti": str(self.jti),
            "iat": self.iat,
            "exp": self.exp,
            "user_id": str(self.user_id),
            "role": self.role.value,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "patronymic": self.patronymic,
        }


@dataclass(frozen=True, eq=True)
class AccessToken:
    payload: Payload

    _ALGORITHM = "HS256"

    def encode(self, secret: str) -> str:
        return jwt.encode(payload=self.payload.to_dict(), key=secret, algorithm=self._ALGORITHM)

    @classmethod
    def generate(cls, user: User) -> "AccessToken":
        now = datetime.now(timezone.utc)

        payload = Payload(
            jti=uuid4(),
            iat=now.timestamp(),
            exp=(now + timedelta(minutes=10)).timestamp(),
            user_id=user.id.value,
            role=user.role,
            last_name=user.name.last.value,
            first_name=user.name.first.value,
            patronymic=user.name.patronymic.value if user.name.patronymic else None,
        )

        return AccessToken(payload)

    @classmethod
    def decode(cls, token: str, secret: str) -> Optional["AccessToken"]:
        try:
            payload = jwt.decode(
                token,
                key=secret,
                algorithms=[cls._ALGORITHM],
                options={"require": ["jti", "iat", "exp", "user_id", "role", "last_name", "first_name", "patronymic"]},
            )

            return AccessToken(Payload.parse_obj(payload))

        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, ValidationError):
            return None


@dataclass(frozen=True, eq=True)
class Fingerprint:
    value: str

    _MAX_LENGTH = 200

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Fingerprint должен быть определён")

        if len(self.value) > self._MAX_LENGTH:
            raise ValueError(f"Длина fingerprint превышает {self._MAX_LENGTH} символов")


@dataclass(frozen=True, eq=True)
class RefreshToken:
    value: UUID

    @classmethod
    def generate(cls) -> "RefreshToken":
        return cls(uuid4())


@dataclass
class Session:
    id: RefreshToken
    user_id: UserID
    fingerprint: Fingerprint
    ip: IPv4Address
    expires_in: datetime
    created_at: datetime

    @property
    def is_expired(self) -> bool:
        return self._now() >= self.expires_in

    @classmethod
    def generate(cls, user: User, ip: IPv4Address, fingerprint: Fingerprint) -> "Session":
        now = cls._now()

        return cls(
            id=RefreshToken.generate(),
            user_id=user.id,
            fingerprint=fingerprint,
            ip=ip,
            expires_in=now + timedelta(days=10),
            created_at=now,
        )

    @staticmethod
    def _now() -> datetime:
        return datetime.now(timezone.utc)
