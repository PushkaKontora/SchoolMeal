class ProcessError(Exception):
    pass


class ProcessHasAlreadyStarted(ProcessError):
    pass


class ProcessHasNotStartedYet(ProcessError):
    pass
