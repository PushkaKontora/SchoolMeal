from uuid import UUID

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.infrastructure.db.base import Base
from app.user.domain.model import (
    Email,
    FirstName,
    HashedPassword,
    LastName,
    Login,
    Phone,
    Photo,
    RefreshToken,
    User,
    UserID,
    UserRole,
)


class UserDB(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[bytes] = mapped_column()
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    role: Mapped[str] = mapped_column(String(32))
    email: Mapped[str | None] = mapped_column(String(32), unique=True)
    phone: Mapped[str | None] = mapped_column(String(12), unique=True)
    photo_url: Mapped[str | None] = mapped_column(String(256))
    authenticated_ips: Mapped[dict[str, str]] = mapped_column(JSON)

    def __init__(
        self,
        id_: UUID,
        login: str,
        hashed_password: bytes,
        first_name: str,
        last_name: str,
        role: str,
        email: str | None,
        phone: str | None,
        photo_url: str | None,
        authenticated_ips: dict[str, str],
    ) -> None:
        super().__init__(
            id=id_,
            login=login,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            phone=phone,
            photo_url=photo_url,
            authenticated_ips=authenticated_ips,
        )

    def to_domain(self) -> User:
        return User(
            id=UserID(self.id),
            role=UserRole(self.role),
            login=Login(self.login),
            hashed_password=HashedPassword(self.hashed_password),
            first_name=FirstName(self.first_name),
            last_name=LastName(self.last_name),
            email=Email(self.email),
            phone=Phone(self.phone),
            photo=Photo(self.photo_url),
            authenticated_ips={
                ip: RefreshToken.decode(refresh_token) for ip, refresh_token in self.authenticated_ips.items()
            },
        )

    @staticmethod
    def from_domain(user: User) -> "UserDB":
        return UserDB(
            id_=user.id.value,
            login=user.login.value,
            hashed_password=user.hashed_password.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            role=user.role.value,
            email=user.email.value,
            phone=user.phone.value,
            photo_url=user.photo.url,
            authenticated_ips={str(ip): str(refresh_token) for ip, refresh_token in user.authenticated_ips.items()},
        )
