from dataclasses import dataclass
from enum import Enum

from app.context.user_account.application.dto import AccountResponseDTO


class FindMultipleAccountsErrorCode(str, Enum):
    """Error codes when searching for multiple accounts"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindMultipleAccountsResult:
    "Result when searching for multiple accounts"

    # Success
    accounts: list[AccountResponseDTO] | None = None

    # Error fields
    error_code: FindMultipleAccountsErrorCode | None = None
    error_message: str | None = None
