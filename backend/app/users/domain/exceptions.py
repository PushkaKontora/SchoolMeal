from app.exceptions import APIException


class NonUniqueUserDataException(APIException):
    @property
    def message(self) -> str:
        return "Login, phone or email should be unique"


class NotFoundUserByTokenException(APIException):
    @property
    def message(self) -> str:
        return "Not found user"

    @property
    def status_code(self) -> int:
        return 404
