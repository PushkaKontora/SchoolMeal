from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CantRevokeAlreadyRevokedSession(Exception):
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
        :raise CantRevokeAlreadyRevokedSession: сессия уже отозвана
        """

        if self.revoked:
            raise CantRevokeAlreadyRevokedSession

        self.revoked = True
        return self
