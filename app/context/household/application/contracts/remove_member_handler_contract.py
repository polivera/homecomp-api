from abc import ABC, abstractmethod

from app.context.household.application.commands import RemoveMemberCommand
from app.context.household.application.dto import RemoveMemberResult


class RemoveMemberHandlerContract(ABC):
    """Contract for remove member command handler"""

    @abstractmethod
    async def handle(self, command: RemoveMemberCommand) -> RemoveMemberResult:
        """Execute the remove member command"""
        pass
