from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.db.base import DictMixin
from app.shared.domain.personal_info import FullName
from app.shared.domain.user import UserID
from app.user_management.domain.credentials import HashedPassword, Login
from app.user_management.domain.jwt import Fingerprint, RefreshToken, Session
from app.user_management.domain.user import Role, User


class UserManagementBase(DeclarativeBase, DictMixin):
    metadata = MetaData(schema="user_management")


class UserDB(UserManagementBase):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()
    password: Mapped[bytes] = mapped_column()
    role: Mapped[int] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    patronymic: Mapped[str | None] = mapped_column()

    def __init__(
        self,
        id_: UUID,
        login: str,
        password: bytes,
        role: int,
        last_name: str,
        first_name: str,
        patronymic: str | None,
    ) -> None:
        super().__init__()

        self.id = id_
        self.login = login
        self.password = password
        self.role = role
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic

    def to_model(self) -> User:
        return User(
            id=UserID(self.id),
            login=Login(self.login),
            password=HashedPassword(self.password),
            role=Role(self.role),
            name=FullName.create(last=self.last_name, first=self.first_name, patronymic=self.patronymic),
        )

    @classmethod
    def from_model(cls, user: User) -> "UserDB":
        return cls(
            id_=user.id.value,
            login=user.login.value,
            password=user.password.value,
            role=user.role.value,
            last_name=user.name.last.value,
            first_name=user.name.first.value,
            patronymic=user.name.patronymic.value if user.name.patronymic else None,
        )


class SessionDB(UserManagementBase):
    __tablename__ = "session"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(UserDB.id))
    fingerprint: Mapped[str] = mapped_column()
    ip: Mapped[str] = mapped_column()
    expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    def __init__(
        self, id_: UUID, user_id: UUID, fingerprint: str, ip: str, expires_in: datetime, created_at: datetime
    ) -> None:
        super().__init__()

        self.id = id_
        self.user_id = user_id
        self.fingerprint = fingerprint
        self.ip = ip
        self.expires_in = expires_in
        self.created_at = created_at

    def to_model(self) -> Session:
        return Session(
            id=RefreshToken(self.id),
            user_id=UserID(self.user_id),
            fingerprint=Fingerprint(self.fingerprint),
            ip=IPv4Address(self.ip),
            expires_in=self.expires_in,
            created_at=self.created_at,
        )

    @classmethod
    def from_model(cls, session: Session) -> "SessionDB":
        return cls(
            id_=session.id.value,
            user_id=session.user_id.value,
            fingerprint=session.fingerprint.value,
            ip=str(session.ip),
            expires_in=session.expires_in,
            created_at=session.created_at,
        )
