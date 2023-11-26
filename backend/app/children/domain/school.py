from uuid import UUID

from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class SchoolName:
    value: str


class School(BaseModel):
    id: UUID
    name: SchoolName
