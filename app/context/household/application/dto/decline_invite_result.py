from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DeclineInviteErrorCode(str, Enum):
    """Error codes for declining invitation"""

    NOT_INVITED = "NOT_INVITED"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeclineInviteResult:
    """Result of decline invitation operation"""

    # Success field - simple boolean for success case
    success: bool = False

    # Error fields - populated when operation fails
    error_code: Optional[DeclineInviteErrorCode] = None
    error_message: Optional[str] = None
