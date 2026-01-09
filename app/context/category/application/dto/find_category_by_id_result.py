from dataclasses import dataclass
from enum import Enum

from app.context.category.application.dto.category_response_dto import CategoryResponseDTO


class FindCategoryByIdErrorCode(str, Enum):
    """Error codes for find category by ID"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindCategoryByIdResult:
    """Result of find category by ID operation"""

    # Success field - populated when operation succeeds
    category: CategoryResponseDTO | None = None

    # Error fields - populated when operation fails
    error_code: FindCategoryByIdErrorCode | None = None
    error_message: str | None = None
