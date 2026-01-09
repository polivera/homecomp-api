from dataclasses import dataclass
from enum import Enum


class UpdateCategoryErrorCode(str, Enum):
    """Error codes for category update"""

    NOT_FOUND = "NOT_FOUND"
    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class UpdateCategoryResult:
    """Result of category update operation"""

    # Success fields - populated when operation succeeds
    category_id: int | None = None
    category_name: str | None = None

    # Error fields - populated when operation fails
    error_code: UpdateCategoryErrorCode | None = None
    error_message: str | None = None
