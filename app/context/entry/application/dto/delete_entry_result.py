from dataclasses import dataclass
from enum import Enum


class DeleteEntryErrorCode(str, Enum):
    """Error codes for entry deletion"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteEntryResult:
    """Result of delete entry operation"""

    # Success field
    success: bool | None = None

    # Error fields
    error_code: DeleteEntryErrorCode | None = None
    error_message: str | None = None
