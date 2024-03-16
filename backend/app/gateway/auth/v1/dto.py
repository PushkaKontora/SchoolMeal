from pydantic import BaseModel


class LoginBody(BaseModel):
    login: str
    password: str
    fingerprint: str


class RefreshBody(BaseModel):
    fingerprint: str
