from pydantic import BaseModel

from app.identity.domain.jwt import AccessToken


class LoginBody(BaseModel):
    login: str
    password: str
    fingerprint: str


class RefreshBody(BaseModel):
    fingerprint: str


class AccessTokenOut(BaseModel):
    token: str

    @classmethod
    def from_model(cls, token: AccessToken) -> "AccessTokenOut":
        return cls(token=token.value)
