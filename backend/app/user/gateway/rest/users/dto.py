from app.common.gateway.dto import FrontendModel


class RegistrationParentForm(FrontendModel):
    phone: str
    password: str
    first_name: str
    last_name: str
    email: str
