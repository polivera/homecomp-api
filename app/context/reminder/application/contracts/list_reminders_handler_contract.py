"""Contract for list reminders handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.dto import ListRemindersResult
from app.context.reminder.application.queries import ListRemindersQuery


class ListRemindersHandlerContract(ABC):
    """Handler contract for listing reminders"""

    @abstractmethod
    async def handle(self, query: ListRemindersQuery) -> ListRemindersResult:
        """Handle list reminders query"""
        pass
