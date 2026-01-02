"""Command for creating a reminder"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateReminderCommand:
    """Command to create a new reminder"""

    user_id: int
    description: str
    entry_type: str
    currency: str
    amount: float
    frequency: str
    start_date: datetime
    category_id: int
    end_date: datetime | None = None
