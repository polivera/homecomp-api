from abc import ABC, abstractmethod

from app.context.entry.application.dto import FindMultipleEntriesResult
from app.context.entry.application.queries import FindEntriesByAccountMonthQuery


class FindEntriesByAccountMonthHandlerContract(ABC):
    """Contract for find entries by account and month handler"""

    @abstractmethod
    async def handle(self, query: FindEntriesByAccountMonthQuery) -> FindMultipleEntriesResult:
        """Handle find entries by account and month query"""
        pass
