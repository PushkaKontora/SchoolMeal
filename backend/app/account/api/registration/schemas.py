from app.account.domain.email import Email
from app.account.domain.names import FirstName, LastName
from app.account.domain.passwords import Password
from app.account.domain.phone import Phone
from app.common.api.schemas import FrontendModel
from app.common.domain.errors import DomainError


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
