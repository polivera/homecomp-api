"""Query for listing reminder occurrences"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ListOccurrencesQuery:
    """Query to list occurrences for a reminder or user"""

    user_id: int
    reminder_id: int | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    status: str | None = None
