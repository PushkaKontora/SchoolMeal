from uuid import UUID

from pydantic import BaseModel


class Canteen(BaseModel):
    id: UUID
