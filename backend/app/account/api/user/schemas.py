from app.account.domain.credential import Credential
from app.account.domain.user import User
from app.common.api.schemas import FrontendModel


class CredentialOut(FrontendModel):
    id: str
    login: str

    @classmethod
    def from_model(cls, credential: Credential) -> "CredentialOut":
        return cls(
            id=str(credential.id),
            login=credential.login.value,
        )


class UserOut(FrontendModel):
    id: str
    credential: CredentialOut
    last_name: str
    first_name: str
    role: str
    phone: str
    email: str

    @classmethod
    def from_model(cls, user: User) -> "UserOut":
        return cls(
            id=str(user.id),
            credential=CredentialOut.from_model(user.credential),
            last_name=user.last_name.value,
            first_name=user.first_name.value,
            role=user.role.value,
            phone=user.phone.value,
            email=user.email.value,
        )
