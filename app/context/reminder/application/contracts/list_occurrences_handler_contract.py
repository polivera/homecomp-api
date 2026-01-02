"""Contract for list occurrences handler"""

from abc import ABC, abstractmethod

from app.context.reminder.application.dto import ListOccurrencesResult
from app.context.reminder.application.queries import ListOccurrencesQuery


class ListOccurrencesHandlerContract(ABC):
    """Handler contract for listing occurrences"""

    @abstractmethod
    async def handle(self, query: ListOccurrencesQuery) -> ListOccurrencesResult:
        """Handle list occurrences query"""
        pass
