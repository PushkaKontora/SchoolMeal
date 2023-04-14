from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.sql.functions import now

from app.database.sqlalchemy.base import CASCADE, Base


class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    value = Column(LargeBinary(100), nullable=False)
    created_at = Column(DateTime, server_default=now(), nullable=False)


class IssuedToken(Base):
    __tablename__ = "issued_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    value = Column(String(512), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=now(), nullable=False)
