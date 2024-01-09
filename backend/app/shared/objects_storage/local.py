import os.path
from enum import Enum, unique
from pathlib import Path
from uuid import uuid4

from pydantic import BaseSettings, Field

from app.shared.objects_storage.abc import IObjectsStorage


@unique
class Protocol(str, Enum):
    HTTP = "http"
    HTTPS = "https"


class LocalObjectsStorageSettings(BaseSettings):
    protocol: Protocol = Field(env="GATEWAY_PROTOCOL")
    host: str = Field(env="GATEWAY_HOST")
    port: int = Field(env="GATEWAY_PORT")
    base_path: Path = Field(env="MEDIA_PATH")


class LocalObjectsStorage(IObjectsStorage):
    def __init__(self, protocol: Protocol, host: str, port: int, base_path: Path) -> None:
        self._protocol = protocol
        self._host = host
        self._port = port
        self._base_path = base_path

    async def get_url(self, file: Path) -> str | None:
        path = self._base_path / file

        if not path.exists():
            return None

        return f"{self._protocol.value}://{self._host}:{self._port}{path.as_posix()}"

    async def save(self, name: str, content: bytes) -> Path:
        prefix, extension = os.path.splitext(name)
        relative_path = Path(f"{uuid4()}{extension}")

        with open(self._base_path / Path(f"{uuid4()}{extension}"), "wb") as file:
            file.write(content)

        return relative_path
