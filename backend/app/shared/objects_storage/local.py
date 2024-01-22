import os.path
from pathlib import Path
from uuid import uuid4

from pydantic import BaseSettings, Field

from app.shared.objects_storage.abc import IObjectsStorage


class LocalObjectsStorageSettings(BaseSettings):
    base_path: Path = Field(env="MEDIA_PATH")


class LocalObjectsStorage(IObjectsStorage):
    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path

    async def get_uri(self, file: Path) -> str | None:
        path = self._base_path / file

        return path.as_posix() if path.exists() else None

    async def save(self, name: str, content: bytes) -> Path:
        prefix, extension = os.path.splitext(name)
        relative_path = Path(f"{uuid4()}{extension}")

        with open(self._base_path / Path(f"{uuid4()}{extension}"), "wb") as file:
            file.write(content)

        return relative_path
