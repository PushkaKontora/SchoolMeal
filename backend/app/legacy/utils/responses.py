from app.legacy.utils.entity import Entity


class SuccessResponse(Entity):
    msg: str = "Success"


class ErrorDescription(Entity):
    code: str
    msg: str


class ErrorResponse(Entity):
    error: ErrorDescription
