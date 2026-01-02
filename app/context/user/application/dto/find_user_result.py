from dataclasses import dataclass
from enum import Enum


class FindUserErrorCode(str, Enum):
    """Error codes for find user operation"""

    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_USER_ID = "INVALID_USER_ID"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindUserResult:
    """Result of find user operation"""

    # Success fields - populated when operation succeeds
    user_id: int | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None

    # Error fields - populated when operation fails
    error_code: FindUserErrorCode | None = None
    error_message: str | None = None
