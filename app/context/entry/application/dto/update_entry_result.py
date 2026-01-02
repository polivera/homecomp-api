from dataclasses import dataclass
from enum import Enum

from app.context.entry.application.dto.entry_response_dto import EntryResponseDTO


class UpdateEntryErrorCode(str, Enum):
    """Error codes for entry update"""

    NOT_FOUND = "NOT_FOUND"
    ACCOUNT_NOT_BELONGS_TO_USER = "ACCOUNT_NOT_BELONGS_TO_USER"
    CATEGORY_NOT_FOUND = "CATEGORY_NOT_FOUND"
    CATEGORY_NOT_BELONGS_TO_USER = "CATEGORY_NOT_BELONGS_TO_USER"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class UpdateEntryResult:
    """Result of update entry operation"""

    # Success fields
    entry: EntryResponseDTO | None = None

    # Error fields
    error_code: UpdateEntryErrorCode | None = None
    error_message: str | None = None
