from app.exceptions import APIException


class NotFoundPortionException(APIException):
    @property
    def message(self) -> str:
        return "Not found portion"

    @property
    def status_code(self) -> int:
        return 404
