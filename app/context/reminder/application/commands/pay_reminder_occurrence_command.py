"""Command for paying a reminder occurrence"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PayReminderOccurrenceCommand:
    """Command to mark a reminder occurrence as paid"""

    occurrence_id: int
    user_id: int
    amount: float
    date: datetime
    account_id: int
