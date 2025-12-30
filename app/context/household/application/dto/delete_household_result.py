from dataclasses import dataclass
from enum import Enum


class DeleteHouseholdErrorCode(str, Enum):
    """Error codes for delete household operation"""

    NOT_FOUND = "NOT_FOUND"
    NOT_OWNER = "NOT_OWNER"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteHouseholdResult:
    """Result of delete household command"""

    success: bool = False
    error_code: DeleteHouseholdErrorCode | None = None
    error_message: str | None = None
