from abc import ABC, abstractmethod

from app.context.entry.application.commands import DeleteEntryCommand
from app.context.entry.application.dto import DeleteEntryResult


class DeleteEntryHandlerContract(ABC):
    """Contract for delete entry handler"""

    @abstractmethod
    async def handle(self, command: DeleteEntryCommand) -> DeleteEntryResult:
        """Handle delete entry command"""
        pass
