from abc import ABC, abstractmethod

from app.context.household.application.commands import DeleteHouseholdCommand
from app.context.household.application.dto import DeleteHouseholdResult


class DeleteHouseholdHandlerContract(ABC):
    """Contract for delete household command handler"""

    @abstractmethod
    async def handle(self, command: DeleteHouseholdCommand) -> DeleteHouseholdResult:
        """Execute the delete household command"""
        pass
