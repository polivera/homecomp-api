from abc import ABC, abstractmethod

from app.context.household.application.commands import DeclineInviteCommand
from app.context.household.application.dto import DeclineInviteResult


class DeclineInviteHandlerContract(ABC):
    """Contract for decline invite command handler"""

    @abstractmethod
    async def handle(self, command: DeclineInviteCommand) -> DeclineInviteResult:
        """Execute the decline invite command"""
        pass
