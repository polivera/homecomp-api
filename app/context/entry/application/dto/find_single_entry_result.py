from dataclasses import dataclass
from enum import Enum

from app.context.entry.application.dto.entry_response_dto import EntryResponseDTO


class FindSingleEntryErrorCode(str, Enum):
    """Error codes for finding single entry"""

    NOT_FOUND = "NOT_FOUND"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindSingleEntryResult:
    """Result of find single entry operation"""

    # Success field
    entry: EntryResponseDTO | None = None

    # Error fields
    error_code: FindSingleEntryErrorCode | None = None
    error_message: str | None = None
