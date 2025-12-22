import secrets
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class SessionToken:
    """
    Session token value object for session-based authentication.
    Represents a cryptographically secure random token.
    """

    value: str

    @classmethod
    def generate(cls) -> Self:
        """Generate a new cryptographically secure session token."""
        return cls(value=secrets.token_urlsafe(32))

    @classmethod
    def from_string(cls, token: str) -> Self:
        """Create a SessionToken from an existing token string."""
        return cls(value=token)
