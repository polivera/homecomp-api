from dataclasses import dataclass
from enum import Enum
from typing import Optional


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
    error_code: Optional[DeleteAccountErrorCode] = None
    error_message: Optional[str] = None
