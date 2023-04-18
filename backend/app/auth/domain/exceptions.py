class BadCredentialsException(Exception):
    pass


class UnknownTokenTypeException(Exception):
    pass


class InvalidTokenSignatureException(Exception):
    pass


class NotFoundRefreshTokenException(Exception):
    pass


class RefreshWithRevokedTokenException(Exception):
    pass


class TokenExpirationException(Exception):
    pass
