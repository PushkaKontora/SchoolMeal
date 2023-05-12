from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.constants import CASCADE


class Teacher(Base):
    __tablename__ = "teachers"

    class_id: Mapped[int] = mapped_column(ForeignKey("school_classes.id", ondelete=CASCADE), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
