from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.domain.abc import Entity


@dataclass
class Canteen(Entity):
    id: UUID
