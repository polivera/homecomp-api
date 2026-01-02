"""Query for finding a single reminder"""

from dataclasses import dataclass


@dataclass(frozen=True)
class FindReminderQuery:
    """Query to find a reminder by ID"""

    reminder_id: int
    user_id: int
