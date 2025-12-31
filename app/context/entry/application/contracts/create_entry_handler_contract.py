from abc import ABC, abstractmethod

from app.context.entry.application.commands import CreateEntryCommand
from app.context.entry.application.dto import CreateEntryResult


class CreateEntryHandlerContract(ABC):
    """Contract for create entry handler"""

    @abstractmethod
    async def handle(self, command: CreateEntryCommand) -> CreateEntryResult:
        """Handle create entry command"""
        pass
