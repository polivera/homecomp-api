"""Contract for update reminder handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.commands import UpdateReminderCommand
from app.context.reminder.application.dto import UpdateReminderResult


class UpdateReminderHandlerContract(ABC):
    """Handler contract for updating reminders"""

    @abstractmethod
    async def handle(self, command: UpdateReminderCommand) -> UpdateReminderResult:
        """Handle update reminder command"""
        pass
