from app.common.api.schemas import FrontendModel
from app.common.domain.errors import DomainError
from app.users.domain.email import Email
from app.users.domain.names import FirstName, LastName
from app.users.domain.passwords import Password
from app.users.domain.phone import Phone


class IncorrectRegistrationFormError(Exception):
    pass


class ParentRegistrationForm(FrontendModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str

    def to_model(self) -> tuple[FirstName, LastName, Phone, Email, Password]:
        """
        :raise IncorrectRegistrationFormError
        """

        try:
            return (
                FirstName(self.first_name),
                LastName(self.last_name),
                Phone(self.phone),
                Email(self.email),
                Password(self.password),
            )
        except DomainError as error:
            raise IncorrectRegistrationFormError(str(error)) from error
