from uuid import UUID

from pydantic import BaseModel

from app.common.domain.role import Role


class AuthenticatedUser(BaseModel):
    id: UUID
    role: Role
