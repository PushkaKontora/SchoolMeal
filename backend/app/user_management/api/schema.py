from app.shared.api.schemas import FrontendBody
from app.user_management.domain.jwt import AccessToken


class LoginBody(FrontendBody):
    login: str
    password: str
    fingerprint: str


class RefreshBody(FrontendBody):
    fingerprint: str


class AccessTokenOut(FrontendBody):
    token: str

    @classmethod
    def from_model(cls, token: AccessToken) -> "AccessTokenOut":
        return cls(token=token.value)
