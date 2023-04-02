from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from app.config import database


engine = create_async_engine(database.dsn)
Session = async_sessionmaker(engine)

Base: DeclarativeMeta = declarative_base()
