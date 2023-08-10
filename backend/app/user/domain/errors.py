class EmptyLoginError(Exception):
    pass


class EmptyPasswordError(Exception):
    pass


class InvalidPhoneFormatError(Exception):
    pass


class InvalidEmailFormatError(Exception):
    pass


class InvalidPhotoURLError(Exception):
    pass


class EmptyFirstNameError(Exception):
    pass


class EmptyLastNameError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class RevokedTokenError(Exception):
    pass


class TokenExpirationError(Exception):
    pass


class NotFoundUserError(Exception):
    pass


class NotVerifiedPasswordError(Exception):
    pass


class NotUniqueUserDataError(Exception):
    pass
