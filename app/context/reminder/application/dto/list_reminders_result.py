"""Result DTO for list reminders query"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ListRemindersErrorCode(str, Enum):
    """Error codes for list reminders operation"""

    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class ReminderListItem:
    """Single reminder item in list"""

    reminder_id: int
    description: str
    entry_type: str
    currency: str
    frequency: str
    start_date: datetime
    end_date: datetime | None = None
    category_id: int | None = None


@dataclass(frozen=True)
class ListRemindersResult:
    """Result of list reminders operation"""

    # Success fields
    reminders: list[ReminderListItem] | None = None

    # Error fields
    error_code: ListRemindersErrorCode | None = None
    error_message: str | None = None
