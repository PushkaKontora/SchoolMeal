from sqlalchemy import Column, Integer, String

from app.database.sqlalchemy.base import Base


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
