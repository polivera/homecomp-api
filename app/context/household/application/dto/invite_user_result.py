from dataclasses import dataclass
from enum import Enum
from typing import Optional


class InviteUserErrorCode(str, Enum):
    """Error codes for user invitation"""

    ONLY_OWNER_CAN_INVITE = "ONLY_OWNER_CAN_INVITE"
    ALREADY_ACTIVE_MEMBER = "ALREADY_ACTIVE_MEMBER"
    ALREADY_INVITED = "ALREADY_INVITED"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class InviteUserResult:
    """Result of user invitation operation"""

    # Success fields - populated when operation succeeds
    member_id: Optional[int] = None
    household_id: Optional[int] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

    # Error fields - populated when operation fails
    error_code: Optional[InviteUserErrorCode] = None
    error_message: Optional[str] = None
