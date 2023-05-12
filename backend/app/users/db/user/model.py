from datetime import datetime
from enum import Enum as BaseEnum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.db.base import Base


class Role(str, BaseEnum):
    PARENT = "parent"
    TEACHER = "teacher"
    EMPLOYEE = "employee"
    ORGANIZER = "organizer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32), nullable=False)
    login: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(12), nullable=True, unique=True)
    email: Mapped[str | None] = mapped_column(String(32), nullable=True, unique=True)
    photo_path: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)

    passwords = relationship("Password", lazy="raise")
