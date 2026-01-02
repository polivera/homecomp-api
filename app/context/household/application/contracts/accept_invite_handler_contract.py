from abc import ABC, abstractmethod

from app.context.household.application.commands import AcceptInviteCommand
from app.context.household.application.dto import AcceptInviteResult


class AcceptInviteHandlerContract(ABC):
    """Contract for accept invite command handler"""

    @abstractmethod
    async def handle(self, command: AcceptInviteCommand) -> AcceptInviteResult:
        """Execute the accept invite command"""
        pass
