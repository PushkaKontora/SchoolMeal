from abc import ABC, abstractmethod
from pathlib import Path


class IObjectsStorage(ABC):
    @abstractmethod
    async def get_url(self, file: Path) -> str | None:
        raise NotImplementedError
