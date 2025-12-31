from dataclasses import dataclass
from enum import Enum

from app.context.entry.application.dto.entry_response_dto import EntryResponseDTO


class FindMultipleEntriesErrorCode(str, Enum):
    """Error codes for finding multiple entries"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindMultipleEntriesResult:
    """Result of find multiple entries operation"""

    # Success field
    entries: list[EntryResponseDTO] | None = None

    # Error fields
    error_code: FindMultipleEntriesErrorCode | None = None
    error_message: str | None = None
