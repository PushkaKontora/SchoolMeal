from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.database.sqlalchemy.base import CASCADE, Base


class Password(Base):
    __tablename__ = "passwords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    value: Mapped[bytes] = mapped_column(LargeBinary(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)


class IssuedToken(Base):
    __tablename__ = "issued_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    value: Mapped[str] = mapped_column(String(512), nullable=False)
    revoked: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)
