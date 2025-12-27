from abc import ABC, abstractmethod

from app.context.household.application.commands import CreateHouseholdCommand
from app.context.household.application.dto import CreateHouseholdResult


class CreateHouseholdHandlerContract(ABC):
    @abstractmethod
    async def handle(self, command: CreateHouseholdCommand) -> CreateHouseholdResult:
        """Execute the create household command"""
        pass
