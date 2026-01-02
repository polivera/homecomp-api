"""Result DTO for find reminder query"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class FindReminderErrorCode(str, Enum):
    """Error codes for find reminder operation"""

    REMINDER_NOT_FOUND = "REMINDER_NOT_FOUND"
    REMINDER_NOT_BELONGS_TO_USER = "REMINDER_NOT_BELONGS_TO_USER"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class FindReminderResult:
    """Result of find reminder operation"""

    # Success fields
    reminder_id: int | None = None
    description: str | None = None
    entry_type: str | None = None
    currency: str | None = None
    frequency: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    category_id: int | None = None

    # Error fields
    error_code: FindReminderErrorCode | None = None
    error_message: str | None = None
