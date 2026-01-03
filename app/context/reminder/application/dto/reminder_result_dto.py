from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ReminderDTO:
    user_id: int
    category_id: int
    entry_type: str
    currency: str
    amount: float
    frequency: str
    start_date: datetime
    description: str
    end_date: datetime | None = None
    reminder_id: int | None = None
