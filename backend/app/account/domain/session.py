from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.common.domain.errors import DomainError


class AlreadySessionRevokedError(DomainError):
    pass


class Session(BaseModel):
    id: UUID
    jti: UUID
    credential_id: UUID
    device_id: UUID
    revoked: bool
    created_at: datetime

    def revoke(self) -> "Session":
        """
        :raise AlreadyRevokedSessionError: сессия уже отозвана
        """

        if self.revoked:
            raise AlreadySessionRevokedError("Сессия уже отозвана")

        self.revoked = True
        return self
