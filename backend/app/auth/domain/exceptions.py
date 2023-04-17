class BadCredentialsException(Exception):
    pass


class UnknownTokenTypeException(Exception):
    pass


class TokenSignatureException(Exception):
    pass


class UnknownTokenException(Exception):
    pass


class TokenIsRevokedException(Exception):
    pass


class TokenExpirationException(Exception):
    pass
