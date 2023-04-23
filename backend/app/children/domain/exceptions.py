from app.exceptions import APIException


class NotFoundParentException(APIException):
    @property
    def message(self) -> str:
        return "The parent was not found"


class NotFoundChildException(APIException):
    @property
    def message(self) -> str:
        return "The child was not found"


class NotUniqueChildException(APIException):
    @property
    def message(self) -> str:
        return "The child was already added by the user"
