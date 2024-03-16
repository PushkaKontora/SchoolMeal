from datetime import datetime
from ipaddress import IPv4Address
from uuid import UUID

from pydantic import BaseModel

from app.identity.domain.credentials import Login, Password
from app.identity.domain.jwt import AccessToken, Fingerprint, RefreshToken, Secret


class AuthenticationIn(BaseModel):
    login: Login
    password: Password
    ip: IPv4Address
    fingerprint: Fingerprint
    secret: Secret


class RefreshTokensIn(BaseModel):
    token: UUID
    ip: IPv4Address
    fingerprint: Fingerprint
    secret: Secret


class SessionOut(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken
    expires_in: datetime
    created_at: datetime
