from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import now

from app.database.base import Base
from app.database.constants import CASCADE


class Password(Base):
    __tablename__ = "passwords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    value: Mapped[bytes] = mapped_column(LargeBinary(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=now(), nullable=False)
