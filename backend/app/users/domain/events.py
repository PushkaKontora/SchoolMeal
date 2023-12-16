from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.event import Event
from app.shared.event_bus.types import JSON
from app.users.domain.names import FirstName, LastName
from app.users.domain.role import Role


@dataclass(frozen=True)
class UserRegistered(Event):
    id: UUID
    last_name: LastName
    first_name: FirstName
    role: Role

    def to_json(self) -> JSON:
        return {
            "id": str(self.id),
            "last_name": self.last_name.value,
            "first_name": self.first_name.value,
            "role": self.role.value,
        }
