from uuid import UUID, uuid4

from pydantic import BaseModel

from app.account.domain.credential import Credential
from app.account.domain.email import Email
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import Password
from app.account.domain.phone import Phone
from app.account.domain.role import Role


class User(BaseModel):
    id: UUID
    credential: Credential
    last_name: LastName
    first_name: FirstName
    role: Role
    phone: Phone
    email: Email

    @classmethod
    def create_parent(
        cls, first_name: FirstName, last_name: LastName, phone: Phone, email: Email, password: Password
    ) -> "User":
        credential = Credential(
            id=uuid4(),
            login=phone.as_login(),
            password=password.hash(),
        )

        return cls(
            id=uuid4(),
            credential=credential,
            last_name=last_name,
            first_name=first_name,
            role=Role.PARENT,
            phone=phone,
            email=email,
        )
