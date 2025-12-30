from abc import ABC, abstractmethod

from app.context.household.application.commands import UpdateHouseholdCommand
from app.context.household.application.dto import UpdateHouseholdResult


class UpdateHouseholdHandlerContract(ABC):
    """Contract for update household command handler"""

    @abstractmethod
    async def handle(self, command: UpdateHouseholdCommand) -> UpdateHouseholdResult:
        """Execute the update household command"""
        pass
