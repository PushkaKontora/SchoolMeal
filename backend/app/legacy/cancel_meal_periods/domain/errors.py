from app.legacy.utils.error import Error


class UserIsNotParentError(Error):
    @property
    def message(self) -> str:
        return "The user is not a parent of the pupil"

    @property
    def status_code(self) -> int:
        return 403


class NotFoundPeriodError(Error):
    @property
    def message(self) -> str:
        return "Not found period"

    @property
    def status_code(self) -> int:
        return 404
