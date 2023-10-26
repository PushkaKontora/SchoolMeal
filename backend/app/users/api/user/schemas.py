from enum import Enum

from app.common.api.schemas import FrontendModel
from app.users.domain.role import Role
from app.users.domain.user import User


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
