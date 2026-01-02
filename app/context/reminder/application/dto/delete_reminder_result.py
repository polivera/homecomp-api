"""Result DTO for delete reminder command"""

from dataclasses import dataclass
from enum import Enum


class DeleteReminderErrorCode(str, Enum):
    """Error codes for delete reminder operation"""

    REMINDER_NOT_FOUND = "REMINDER_NOT_FOUND"
    REMINDER_NOT_BELONGS_TO_USER = "REMINDER_NOT_BELONGS_TO_USER"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass(frozen=True)
class DeleteReminderResult:
    """Result of delete reminder operation"""

    # Success field
    deleted: bool = False

    # Error fields
    error_code: DeleteReminderErrorCode | None = None
    error_message: str | None = None
