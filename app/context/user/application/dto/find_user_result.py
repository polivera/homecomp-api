from dataclasses import dataclass
from enum import Enum
from typing import Optional


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
    user_id: Optional[int] = None
    email: Optional[str] = None
    username: Optional[str] = None

    # Error fields - populated when operation fails
    error_code: Optional[FindUserErrorCode] = None
    error_message: Optional[str] = None
