"""Contract for find reminder handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.dto import FindReminderResult
from app.context.reminder.application.queries import FindReminderQuery


class FindReminderHandlerContract(ABC):
    """Handler contract for finding a reminder"""

    @abstractmethod
    async def handle(self, query: FindReminderQuery) -> FindReminderResult:
        """Handle find reminder query"""
        pass
