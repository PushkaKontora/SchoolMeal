from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from app.database.sqlalchemy.base import CASCADE, Base


class MealRequest(Base):
    __tablename__ = "meal_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("users.id", ondelete=CASCADE), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=now(), nullable=False)

    declared_pupils = relationship("DeclaredPupils")


class DeclaredPupils(Base):
    __tablename__ = "declared_pupils"

    request_id = Column(Integer, ForeignKey("meal_requests.id", ondelete=CASCADE), primary_key=True)
    pupil_id = Column(String, ForeignKey("pupils.id", ondelete=CASCADE), primary_key=True)
    breakfast = Column(Boolean, nullable=False)
    lunch = Column(Boolean, nullable=False)
    dinner = Column(Boolean, nullable=False)
    preferential = Column(Boolean, nullable=False)
