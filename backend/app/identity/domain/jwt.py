from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from ipaddress import IPv4Address
from uuid import UUID, uuid4

import jwt
from pydantic import BaseModel, ValidationError

from app.identity.domain.user import Role, User
from app.shared.domain.user import UserID


@dataclass(frozen=True, eq=True)
class Secret:
    value: str


class Payload(BaseModel):
    jti: UUID
    user_id: UUID
    role: Role
    iat: float
    exp: float


@dataclass(frozen=True, eq=True)
class AccessToken:
    value: str

    _ALGORITHM = "HS256"

    @classmethod
    def generate(cls, user: User, secret: Secret) -> "AccessToken":
        now = datetime.now(timezone.utc)

        payload = {
            "jti": str(uuid4()),
            "user_id": str(user.id.value),
            "role": user.role.value,
            "iat": now.timestamp(),
            "exp": (now + timedelta(minutes=10)).timestamp(),
        }

        return AccessToken(jwt.encode(payload, key=secret.value, algorithm=cls._ALGORITHM))

    @classmethod
    def decode(cls, token: str, secret: Secret) -> Payload | None:
        try:
            payload = jwt.decode(
                token,
                key=secret.value,
                algorithms=[cls._ALGORITHM],
                options={"require": ["jti", "user_id", "role", "iat", "exp"]},
            )

            return Payload.parse_obj(payload)

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
