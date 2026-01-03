"""Result DTO for pay reminder occurrence command"""

from dataclasses import dataclass
from enum import Enum


class PayReminderOccurrenceErrorCode(str, Enum):
    """Error codes for pay reminder occurrence operation"""

    OCCURRENCE_NOT_FOUND = "OCCURRENCE_NOT_FOUND"
    OCCURRENCE_NOT_BELONGS_TO_USER = "OCCURRENCE_NOT_BELONGS_TO_USER"
    OCCURRENCE_ALREADY_PAID = "OCCURRENCE_ALREADY_PAID"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class PayReminderOccurrenceResult:
    """Result of pay reminder occurrence operation"""

    # Success fields
    paid: bool = False
    entry_id: int | None = None

    # Error fields
    error_code: PayReminderOccurrenceErrorCode | None = None
    error_message: str | None = None
