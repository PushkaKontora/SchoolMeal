from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as UUID_DB
from sqlalchemy.orm import Mapped, relationship

from app.account.domain.credential import Credential
from app.account.domain.email import Email
from app.account.domain.login import Login
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import HashedPassword
from app.account.domain.phone import Phone
from app.account.domain.role import Role
from app.account.domain.session import Session
from app.account.domain.user import User
from app.common.infrastructure.db.base import Base


class CredentialDB(Base):
    __tablename__ = "credential"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    login: Mapped[str] = Column(String(256), nullable=False, unique=True)
    password: Mapped[str] = Column(String(256), nullable=False)

    def to_model(self) -> Credential:
        return Credential(
            id=self.id,
            login=Login(self.login),
            password=HashedPassword(self.password.encode("utf-8")),
        )

    @classmethod
    def from_model(cls, credential: Credential) -> "CredentialDB":
        return cls(
            id=credential.id,
            login=credential.login.value,
            password=credential.password.value.decode("utf-8"),
        )


class SessionDB(Base):
    __tablename__ = "session"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    jti: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    credential_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    device_id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), nullable=False)
    revoked: Mapped[bool] = Column(Boolean, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime(timezone=True), nullable=False)

    def to_model(self) -> Session:
        return Session(
            id=self.id,
            jti=self.jti,
            credential_id=self.credential_id,
            device_id=self.device_id,
            revoked=self.revoked,
            created_at=self.created_at,
        )

    @classmethod
    def from_model(cls, session: Session) -> "SessionDB":
        return cls(
            id=session.id,
            jti=session.jti,
            credential_id=session.credential_id,
            device_id=session.device_id,
            revoked=session.revoked,
            created_at=session.created_at,
        )


class UserDB(Base):
    __tablename__ = "user"

    id: Mapped[UUID] = Column(UUID_DB(as_uuid=True), primary_key=True)
    credential_id: Mapped[UUID] = Column(ForeignKey(CredentialDB.id), nullable=False)
    last_name: Mapped[str] = Column(String(256), nullable=False)
    first_name: Mapped[str] = Column(String(256), nullable=False)
    role: Mapped[str] = Column(String(32), nullable=False)
    phone: Mapped[str] = Column(String(32), nullable=False)
    email: Mapped[str] = Column(String(128), nullable=False)

    credential: Mapped[CredentialDB] = relationship(CredentialDB, uselist=False, lazy="joined")

    def to_model(self) -> User:
        return User(
            id=self.id,
            credential=self.credential.to_model(),
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
            credential=CredentialDB.from_model(user.credential),
            last_name=user.last_name.value,
            first_name=user.first_name.value,
            role=user.role.value,
            phone=user.phone.value,
            email=user.email.value,
        )
