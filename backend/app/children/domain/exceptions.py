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


class UserIsNotParentOfThePupilException(APIException):
    @property
    def message(self) -> str:
        return "The user is not a parent of the pupil"

    @property
    def status_code(self) -> int:
        return 403
