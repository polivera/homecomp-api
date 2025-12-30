from dataclasses import dataclass
from enum import Enum


class UpdateHouseholdErrorCode(str, Enum):
    """Error codes for update household operation"""

    NOT_FOUND = "NOT_FOUND"
    NOT_OWNER = "NOT_OWNER"
    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class UpdateHouseholdResult:
    """Result of update household command"""

    # Success fields - populated when operation succeeds
    household_id: int | None = None
    household_name: str | None = None
    owner_user_id: int | None = None

    # Error fields - populated when operation fails
    error_code: UpdateHouseholdErrorCode | None = None
    error_message: str | None = None
