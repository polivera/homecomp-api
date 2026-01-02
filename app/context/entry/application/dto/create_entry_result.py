from dataclasses import dataclass
from enum import Enum


class CreateEntryErrorCode(str, Enum):
    """Error codes for entry creation"""

    ACCOUNT_NOT_BELONGS_TO_USER = "ACCOUNT_NOT_BELONGS_TO_USER"
    CATEGORY_NOT_FOUND = "CATEGORY_NOT_FOUND"
    CATEGORY_NOT_BELONGS_TO_USER = "CATEGORY_NOT_BELONGS_TO_USER"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateEntryResult:
    """Result of create entry operation"""

    # Success fields
    entry_id: int | None = None
    account_id: int | None = None
    category_id: int | None = None
    entry_type: str | None = None
    entry_date: str | None = None  # ISO format
    amount: float | None = None
    description: str | None = None

    # Error fields
    error_code: CreateEntryErrorCode | None = None
    error_message: str | None = None
