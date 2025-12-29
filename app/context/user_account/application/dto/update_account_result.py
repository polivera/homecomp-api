from dataclasses import dataclass
from enum import Enum


class UpdateAccountErrorCode(str, Enum):
    """Error codes for account update"""

    NOT_FOUND = "NOT_FOUND"
    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class UpdateAccountResult:
    """Result of account update operation"""

    # Success fields - populated when operation succeeds
    account_id: int | None = None
    account_name: str | None = None
    account_balance: float | None = None

    # Error fields - populated when operation fails
    error_code: UpdateAccountErrorCode | None = None
    error_message: str | None = None
