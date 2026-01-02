"""Command for updating a reminder"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class UpdateReminderCommand:
    """Command to update an existing reminder"""

    reminder_id: int
    user_id: int
    description: str | None = None
    entry_type: str | None = None
    currency: str | None = None
    frequency: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    category_id: int | None = None
