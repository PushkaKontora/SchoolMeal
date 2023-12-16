from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionIsAlreadyRevoked(Exception):
    pass


class Session(BaseModel):
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
