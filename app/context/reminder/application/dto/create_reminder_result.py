"""Result DTO for create reminder command"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CreateReminderErrorCode(str, Enum):
    """Error codes for create reminder operation"""

    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    INVALID_FREQUENCY = "INVALID_FREQUENCY"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateReminderResult:
    """Result of create reminder operation"""

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
    error_code: CreateReminderErrorCode | None = None
    error_message: str | None = None
