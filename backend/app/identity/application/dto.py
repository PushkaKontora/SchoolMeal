from ipaddress import IPv4Address
from uuid import UUID

from pydantic import BaseModel

from app.identity.domain.credentials import Login, Password
from app.identity.domain.jwt import Fingerprint, Secret


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
