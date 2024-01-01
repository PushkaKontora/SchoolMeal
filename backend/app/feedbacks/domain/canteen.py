from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.domain import Entity


@dataclass
class Canteen(Entity):
    id: UUID
