from enum import Enum

from app.shared.fastapi.schemas import FrontendModel
from app.users.domain.role import Role
from app.users.domain.tokens import AccessToken
from app.users.domain.user import User


class CredentialIn(FrontendModel):
    login: str
    password: str


class AccessTokenOut(FrontendModel):
    access_token: str

    @classmethod
    def from_model(cls, access_token: AccessToken, secret: str) -> "AccessTokenOut":
        return cls(access_token=access_token.encode(secret))


class RoleOut(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    MEAL_ORGANIZER = "meal_organizer"
    CANTEEN_STAFF = "canteen_staff"

    @classmethod
    def from_model(cls, role: Role) -> "RoleOut":
        return cls(role.value)


class UserOut(FrontendModel):
    id: str
    login: str
    last_name: str
    first_name: str
    role: RoleOut
    phone: str
    email: str

    @classmethod
    def from_model(cls, user: User) -> "UserOut":
        return cls(
            id=str(user.id),
            login=user.login.value,
            last_name=user.last_name.value,
            first_name=user.first_name.value,
            role=RoleOut.from_model(user.role),
            phone=user.phone.value,
            email=user.email.value,
        )


class ParentRegistrationForm(FrontendModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str
