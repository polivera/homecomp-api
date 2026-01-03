"""Result DTO for create reminder command"""

from dataclasses import dataclass
from enum import Enum

from app.context.reminder.domain.dto import ReminderDTO


class CreateReminderErrorCode(str, Enum):
    """Error codes for create reminder operation"""

    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    INVALID_FREQUENCY = "INVALID_FREQUENCY"
    MAPPER_ERROR = "MAPPER_ERROR"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class CreateReminderResult:
    """Result of create reminder operation"""

    # Success field
    reminder: ReminderDTO | None = None

    # Error fields
    error_code: CreateReminderErrorCode | None = None
    error_message: str | None = None
