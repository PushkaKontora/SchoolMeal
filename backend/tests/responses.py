def error(code: str, message: str) -> dict:
    return {"error": {"code": code, "msg": message}}


SUCCESS = {"msg": "Success"}
UNAUTHORIZED = error("BadCredentialsException", "Incorrect login or password")
FORBIDDEN = error("ForbiddenError", "Permission denied")
NOT_FOUND = error("NotFoundError", "Not found")
