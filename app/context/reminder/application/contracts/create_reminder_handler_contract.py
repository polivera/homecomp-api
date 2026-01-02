"""Contract for create reminder handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.commands import CreateReminderCommand
from app.context.reminder.application.dto import CreateReminderResult


class CreateReminderHandlerContract(ABC):
    """Handler contract for creating reminders"""

    @abstractmethod
    async def handle(self, command: CreateReminderCommand) -> CreateReminderResult:
        """Handle create reminder command"""
        pass
