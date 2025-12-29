from dataclasses import dataclass
from enum import Enum


class DeleteAccountErrorCode(str, Enum):
    """Error codes for account deletion"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteAccountResult:
    """Result of account deletion operation"""

    # Success field - populated when operation succeeds
    success: bool = False

    # Error fields - populated when operation fails
    error_code: DeleteAccountErrorCode | None = None
    error_message: str | None = None
