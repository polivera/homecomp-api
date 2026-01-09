from dataclasses import dataclass
from enum import Enum


class CreateCategoryErrorCode(str, Enum):
    """Error codes for category creation"""

    NAME_ALREADY_EXISTS = "NAME_ALREADY_EXISTS"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateCategoryResult:
    """Result of category creation operation"""

    # Success fields - populated when operation succeeds
    category_id: int | None = None
    category_name: str | None = None

    # Error fields - populated when operation fails
    error_code: CreateCategoryErrorCode | None = None
    error_message: str | None = None
