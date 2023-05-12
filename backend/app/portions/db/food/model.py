from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.constants import CASCADE


class Food(Base):
    __tablename__ = "foods"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id", ondelete=CASCADE), nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    photo_path: Mapped[str] = mapped_column(String(128), nullable=True)
