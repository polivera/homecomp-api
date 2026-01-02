from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class HouseholdSummary:
    """Summary of household for list response"""

    household_id: int
    household_name: str
    owner_user_id: int
    created_at: str


class ListUserHouseholdsErrorCode(str, Enum):
    """Error codes for list user households operation"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class ListUserHouseholdsResult:
    """Result of list user households query"""

    # Success field - populated when operation succeeds
    households: list[HouseholdSummary] | None = None

    # Error fields - populated when operation fails
    error_code: ListUserHouseholdsErrorCode | None = None
    error_message: str | None = None
