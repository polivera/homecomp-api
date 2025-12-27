from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CreateHouseholdErrorCode(str, Enum):
    """Error codes for household creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateHouseholdResult:
    """Result of household creation operation"""

    # Success fields - populated when operation succeeds
    household_id: Optional[int] = None
    household_name: Optional[str] = None

    # Error fields - populated when operation fails
    error_code: Optional[CreateHouseholdErrorCode] = None
    error_message: Optional[str] = None
