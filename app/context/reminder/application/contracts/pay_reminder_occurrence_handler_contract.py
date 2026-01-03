"""Contract for pay reminder occurrence handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.commands import PayReminderOccurrenceCommand
from app.context.reminder.application.dto import PayReminderOccurrenceResult


class PayReminderOccurrenceHandlerContract(ABC):
    """Contract for handler that processes pay reminder occurrence commands"""

    @abstractmethod
    async def handle(self, command: PayReminderOccurrenceCommand) -> PayReminderOccurrenceResult:
        """Execute pay reminder occurrence command"""
        pass
