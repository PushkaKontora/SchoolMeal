from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.identity.application import dto


class SessionOut(BaseModel):
    access_token: str
    refresh_token: UUID
    expires_in: datetime
    created_at: datetime

    @classmethod
    def from_application(cls, session_out: dto.SessionOut) -> "SessionOut":
        return cls(
            access_token=session_out.access_token.value,
            refresh_token=session_out.refresh_token.value,
            expires_in=session_out.expires_in,
            created_at=session_out.created_at,
        )
