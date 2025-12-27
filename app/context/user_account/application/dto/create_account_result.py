from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CreateAccountErrorCode(str, Enum):
    """Error codes for account creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateAccountResult:
    """Result of account creation operation"""

    # Success fields - populated when operation succeeds
    account_id: Optional[int] = None
    account_name: Optional[str] = None
    account_balance: Optional[float] = None

    # Error fields - populated when operation fails
    error_code: Optional[CreateAccountErrorCode] = None
    error_message: Optional[str] = None
