from dataclasses import dataclass
from enum import Enum


class RemoveMemberErrorCode(str, Enum):
    """Error codes for removing member"""

    ONLY_OWNER_CAN_REMOVE = "ONLY_OWNER_CAN_REMOVE"
    CANNOT_REMOVE_SELF = "CANNOT_REMOVE_SELF"
    MEMBER_NOT_FOUND = "MEMBER_NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class RemoveMemberResult:
    """Result of remove member operation"""

    # Success field - simple boolean for success case
    success: bool = False

    # Error fields - populated when operation fails
    error_code: RemoveMemberErrorCode | None = None
    error_message: str | None = None
