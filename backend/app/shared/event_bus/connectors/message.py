import json
from datetime import datetime
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.event_bus.types import JSON


@dataclass
class Message:
    id: UUID
    data: JSON
    created_at: datetime

    def to_bytes(self) -> bytes:
        payload = {
            "id": str(self.id),
            "data": self.data,
            "created_at": self.created_at.isoformat(),
        }
        return json.dumps(payload).encode()
