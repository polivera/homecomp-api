from abc import ABC, abstractmethod

from app.context.entry.application.dto import FindSingleEntryResult
from app.context.entry.application.queries import FindEntryByIdQuery


class FindEntryByIdHandlerContract(ABC):
    """Contract for find entry by ID handler"""

    @abstractmethod
    async def handle(self, query: FindEntryByIdQuery) -> FindSingleEntryResult:
        """Handle find entry by ID query"""
        pass
