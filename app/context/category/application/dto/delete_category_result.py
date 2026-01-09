from dataclasses import dataclass
from enum import Enum


class DeleteCategoryErrorCode(str, Enum):
    """Error codes for category deletion"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteCategoryResult:
    """Result of category deletion operation"""

    # Success field - populated when operation succeeds
    deleted: bool | None = None

    # Error fields - populated when operation fails
    error_code: DeleteCategoryErrorCode | None = None
    error_message: str | None = None
