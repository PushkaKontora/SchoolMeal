from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped

from app.shared.db.base import Base
from app.users.domain.email import Email
from app.users.domain.login import Login
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import HashedPassword
from app.users.domain.phone import Phone
from app.users.domain.role import Role
from app.users.domain.session import Session
from app.users.domain.user import User


class UsersSchemaMixin:
    __table_args__ = {"schema": "users"}


class SessionDB(Base, UsersSchemaMixin):
    __tablename__ = "session"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    jti: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    user_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    device_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    revoked: Mapped[bool] = Column(Boolean, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    def to_model(self) -> Session:
        return Session(
            id=self.id,
            jti=self.jti,
            user_id=self.user_id,
            device_id=self.device_id,
            revoked=self.revoked,
            created_at=self.created_at,
        )

    @classmethod
    def from_model(cls, session: Session) -> "SessionDB":
        return cls(
            id=session.id,
            jti=session.jti,
            user_id=session.user_id,
            device_id=session.device_id,
            revoked=session.revoked,
            created_at=session.created_at,
        )


class UserDB(Base, UsersSchemaMixin):
    __tablename__ = "user"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    login: Mapped[str] = Column(String(256), nullable=False, unique=True)
    password: Mapped[str] = Column(String(256), nullable=False)
    last_name: Mapped[str] = Column(String(256), nullable=False)
    first_name: Mapped[str] = Column(String(256), nullable=False)
    role: Mapped[str] = Column(String(32), nullable=False)
    phone: Mapped[str] = Column(String(32), nullable=False)
    email: Mapped[str] = Column(String(128), nullable=False)

    def to_model(self) -> User:
        return User(
            id=self.id,
            login=Login(self.login),
            password=HashedPassword(self.password.encode("utf-8")),
            last_name=LastName(self.last_name),
            first_name=FirstName(self.first_name),
            role=Role(self.role),
            phone=Phone(self.phone),
            email=Email(self.email),
        )

    @classmethod
    def from_model(cls, user: User) -> "UserDB":
        return UserDB(
            id=user.id,
            login=user.login.value,
            password=user.password.value.decode("utf-8"),
            last_name=user.last_name.value,
            first_name=user.first_name.value,
            role=user.role.value,
            phone=user.phone.value,
            email=user.email.value,
        )
