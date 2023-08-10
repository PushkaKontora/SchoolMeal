from app.legacy.utils.error import Error


class NonUniqueUserDataError(Error):
    @property
    def message(self) -> str:
        return "Login, phone or email should be unique"


class NotFoundUserError(Error):
    @property
    def message(self) -> str:
        return "Not found user"

    @property
    def status_code(self) -> int:
        return 404
