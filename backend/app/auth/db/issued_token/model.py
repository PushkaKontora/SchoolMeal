from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import now

from app.db.base import Base
from app.db.constants import CASCADE


class IssuedToken(Base):
    __tablename__ = "issued_tokens"

    value: Mapped[str] = mapped_column(String(512), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    revoked: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)
