"""Contract for delete reminder handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.commands import DeleteReminderCommand
from app.context.reminder.application.dto import DeleteReminderResult


class DeleteReminderHandlerContract(ABC):
    """Handler contract for deleting reminders"""

    @abstractmethod
    async def handle(self, command: DeleteReminderCommand) -> DeleteReminderResult:
        """Handle delete reminder command"""
        pass
