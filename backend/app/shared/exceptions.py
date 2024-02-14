class DomainException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

        self.message = message


class ApplicationException(Exception):
    pass


class InfrastructureException(Exception):
    pass
