from app.common.gateway.dto import FrontendModel


class CredentialsIn(FrontendModel):
    login: str
    password: str


class AccessTokenOut(FrontendModel):
    access_token: str
