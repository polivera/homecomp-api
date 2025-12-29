from dataclasses import dataclass
from enum import Enum


class AcceptInviteErrorCode(str, Enum):
    """Error codes for accepting invitation"""

    NOT_INVITED = "NOT_INVITED"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class AcceptInviteResult:
    """Result of accept invitation operation"""

    # Success fields - populated when operation succeeds
    member_id: int | None = None
    household_id: int | None = None
    user_id: int | None = None
    role: str | None = None

    # Error fields - populated when operation fails
    error_code: AcceptInviteErrorCode | None = None
    error_message: str | None = None
