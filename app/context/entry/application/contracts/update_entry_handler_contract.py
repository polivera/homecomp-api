from abc import ABC, abstractmethod

from app.context.entry.application.commands import UpdateEntryCommand
from app.context.entry.application.dto import UpdateEntryResult


class UpdateEntryHandlerContract(ABC):
    """Contract for update entry handler"""

    @abstractmethod
    async def handle(self, command: UpdateEntryCommand) -> UpdateEntryResult:
        """Handle update entry command"""
        pass
