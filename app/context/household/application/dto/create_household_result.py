from dataclasses import dataclass
from enum import Enum


class CreateHouseholdErrorCode(str, Enum):
    """Error codes for household creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateHouseholdResult:
    """Result of household creation operation"""

    # Success fields - populated when operation succeeds
    household_id: int | None = None
    household_name: str | None = None

    # Error fields - populated when operation fails
    error_code: CreateHouseholdErrorCode | None = None
    error_message: str | None = None
