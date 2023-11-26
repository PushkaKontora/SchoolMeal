from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from loguru import logger
from psycopg2 import connect
from pydantic import BaseSettings, Field
from pydantic.dataclasses import dataclass


class DatabaseSettings(BaseSettings):
    user: str = Field(env="DB_USER")
    password: str = Field(env="DB_PASSWORD")
    host: str = Field(env="DB_HOST")
    port: int = Field(env="DB_PORT")
    database: str = Field(env="DB_NAME")


class Connection:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings

    def __enter__(self) -> "Database":
        self._connection = connect(
            user=self._settings.user,
            password=self._settings.password,
            host=self._settings.host,
            port=self._settings.port,
            database=self._settings.database,
        )
        self._cursor = self._connection.cursor()

        logger.success(f"Установлено подключение с БД {self._settings.json()}")

        return Database(cursor=self._cursor)

    def __exit__(self, *args: Any) -> None:
        self._connection.commit()
        self._connection.close()
        self._cursor.close()


class Database:
    def __init__(self, cursor: Any) -> None:
        self._cursor = cursor

    def insert(self, schema: str, table: str, data: dict[str, "DBObject"]) -> "Database":
        query = f"INSERT INTO {schema}.{table} ({','.join(data.keys())}) VALUES ({','.join(map(str, data.values()))});"
        self._cursor.execute(query)
        return self

    def truncate(self, schema: str, table: str) -> "Database":
        query = f"TRUNCATE TABLE {schema}.{table} CASCADE;"
        self._cursor.execute(query)
        return self


@dataclass(eq=True, frozen=True, repr=False)
class DBObject(ABC):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __repr__(self) -> str:
        return str(self)


@dataclass(eq=True, frozen=True, repr=False)
class String(DBObject):
    value: str

    def __str__(self) -> str:
        return f"'{self.value}'"


@dataclass(eq=True, frozen=True, repr=False)
class Integer(DBObject):
    value: int

    def __str__(self) -> str:
        return f"{self.value}"


T = TypeVar("T", bound=DBObject)


@dataclass(eq=True, frozen=True, repr=False)
class Array(DBObject, Generic[T]):
    value: tuple[T]

    def __str__(self) -> str:
        _values = ",".join(str(v) for v in self.value)

        return "{" + _values + "}"


@dataclass(eq=True, frozen=True, repr=False)
class Dict(DBObject):
    value: dict[DBObject, DBObject]

    def __str__(self) -> str:
        _values = str(self.value).replace("'", '"')

        return f"'{_values}'"
