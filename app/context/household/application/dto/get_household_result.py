from dataclasses import dataclass
from enum import Enum


class GetHouseholdErrorCode(str, Enum):
    """Error codes for get household operation"""

    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED_ACCESS = "UNAUTHORIZED_ACCESS"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class GetHouseholdResult:
    """Result of get household query"""

    # Success fields - populated when operation succeeds
    household_id: int | None = None
    household_name: str | None = None
    owner_user_id: int | None = None
    created_at: str | None = None

    # Error fields - populated when operation fails
    error_code: GetHouseholdErrorCode | None = None
    error_message: str | None = None
