"""Query for listing user reminders"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ListRemindersQuery:
    """Query to list reminders for a user"""

    user_id: int
    active_only: bool | None = True
