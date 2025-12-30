from dataclasses import dataclass
from enum import Enum

from app.context.user_account.application.dto import AccountResponseDTO


class FindSingleAccountErrorCode(str, Enum):
    """Error codes when searching for single account"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindSingleAccountResult:
    "Result when searching for single account"

    # Success
    account: AccountResponseDTO | None = None

    # Error fields
    error_code: FindSingleAccountErrorCode | None = None
    error_message: str | None = None
