from pydantic import BaseModel


class APIError(BaseModel):
    message: str


class DomainValidationError(APIError):
    pass
