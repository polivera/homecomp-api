from dataclasses import dataclass
from enum import Enum


class CreateAccountErrorCode(str, Enum):
    """Error codes for account creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateAccountResult:
    """Result of account creation operation"""

    # Success fields - populated when operation succeeds
    account_id: int | None = None
    account_name: str | None = None
    account_balance: float | None = None

    # Error fields - populated when operation fails
    error_code: CreateAccountErrorCode | None = None
    error_message: str | None = None
