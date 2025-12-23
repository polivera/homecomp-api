"""Domain exceptions for Auth context."""


class AuthDomainException(Exception):
    """Base exception for Auth domain errors."""

    pass


class InvalidCredentialsException(AuthDomainException):
    """Raised when login credentials are invalid."""

    pass


class AccountBlockedException(AuthDomainException):
    """Raised when account is temporarily blocked due to failed login attempts."""

    def __init__(self, blocked_until: str):
        self.blocked_until = blocked_until
        super().__init__(f"Account is blocked until {blocked_until}")
