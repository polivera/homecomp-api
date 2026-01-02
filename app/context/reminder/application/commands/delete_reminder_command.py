"""Command for deleting a reminder"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteReminderCommand:
    """Command to delete a reminder"""

    reminder_id: int
    user_id: int
