from datetime import datetime
from uuid import UUID

from pydantic.dataclasses import dataclass

from app.shared.domain.abc import Entity


class SessionIsAlreadyRevoked(Exception):
    pass


@dataclass
class Session(Entity):
    id: UUID
    jti: UUID
    user_id: UUID
    device_id: UUID
    revoked: bool
    created_at: datetime

    def revoke(self) -> "Session":
        """
        :raise SessionIsAlreadyRevoked: сессия уже отозвана
        """

        if self.revoked:
            raise SessionIsAlreadyRevoked

        self.revoked = True
        return self
