from app.legacy.utils.error import Error


class NotFoundPortionError(Error):
    @property
    def message(self) -> str:
        return "Not found portion"

    @property
    def status_code(self) -> int:
        return 404
