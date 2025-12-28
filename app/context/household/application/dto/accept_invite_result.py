from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AcceptInviteErrorCode(str, Enum):
    """Error codes for accepting invitation"""

    NOT_INVITED = "NOT_INVITED"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class AcceptInviteResult:
    """Result of accept invitation operation"""

    # Success fields - populated when operation succeeds
    member_id: Optional[int] = None
    household_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

    # Error fields - populated when operation fails
    error_code: Optional[AcceptInviteErrorCode] = None
    error_message: Optional[str] = None
