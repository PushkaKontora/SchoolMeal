from app.legacy.utils.error import Error


class NotFoundParentError(Error):
    @property
    def message(self) -> str:
        return "The parent was not found"


class NotFoundChildError(Error):
    @property
    def message(self) -> str:
        return "The child was not found"


class NotUniqueChildError(Error):
    @property
    def message(self) -> str:
        return "The child was already added by the user"


class UserIsNotParentOfThePupilError(Error):
    @property
    def message(self) -> str:
        return "The user is not a parent of the pupil"

    @property
    def status_code(self) -> int:
        return 403
