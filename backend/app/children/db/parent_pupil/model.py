from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.constants import CASCADE


class ParentPupil(Base):
    __tablename__ = "parents_pupils"

    pupil_id: Mapped[str] = mapped_column(ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete=CASCADE), primary_key=True)
