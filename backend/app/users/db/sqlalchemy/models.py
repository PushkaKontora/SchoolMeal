from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import now

from app.database.sqlalchemy.base import Base
from app.users.domain.entities import Role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    last_name = Column(String(32), nullable=False)
    first_name = Column(String(32), nullable=False)
    login = Column(String(32), nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    phone = Column(String(12), nullable=True, unique=True)
    email = Column(String(32), nullable=True, unique=True)
    photo_path = Column(String(128), nullable=True)
    created_at = Column(DateTime, server_default=now(), nullable=False)

    passwords = relationship("Password", backref="user")
    children = relationship("Pupil", secondary="children", back_populates="parents")
