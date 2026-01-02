"""Result DTO for list occurrences query"""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class ListOccurrencesErrorCode(str, Enum):
    """Error codes for list occurrences operation"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class OccurrenceListItem:
    """Single occurrence item in list"""

    occurrence_id: int
    reminder_id: int
    scheduled_date: datetime
    amount: Decimal
    status: str
    entry_id: int | None = None
    description: str | None = None
    entry_type: str | None = None
    currency: str | None = None
    category_id: int | None = None


@dataclass(frozen=True)
class ListOccurrencesResult:
    """Result of list occurrences operation"""

    # Success fields
    occurrences: list[OccurrenceListItem] | None = None

    # Error fields
    error_code: ListOccurrencesErrorCode | None = None
    error_message: str | None = None
