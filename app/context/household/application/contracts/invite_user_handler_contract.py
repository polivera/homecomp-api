from abc import ABC, abstractmethod

from app.context.household.application.commands import InviteUserCommand
from app.context.household.application.dto import InviteUserResult


class InviteUserHandlerContract(ABC):
    """Contract for invite user command handler"""

    @abstractmethod
    async def handle(self, command: InviteUserCommand) -> InviteUserResult:
        """Execute the invite user command"""
        pass
