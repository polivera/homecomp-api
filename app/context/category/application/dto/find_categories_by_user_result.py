from dataclasses import dataclass
from enum import Enum

from app.context.category.application.dto.category_response_dto import CategoryResponseDTO


class FindCategoriesByUserErrorCode(str, Enum):
    """Error codes for find categories by user"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindCategoriesByUserResult:
    """Result of find categories by user operation"""

    # Success field - populated when operation succeeds
    categories: list[CategoryResponseDTO] | None = None

    # Error fields - populated when operation fails
    error_code: FindCategoriesByUserErrorCode | None = None
    error_message: str | None = None
