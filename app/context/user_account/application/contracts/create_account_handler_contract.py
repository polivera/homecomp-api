from abc import ABC, abstractmethod

from app.context.user_account.application.commands.create_account_command import CreateAccountCommand
from app.context.user_account.application.dto.create_account_result import CreateAccountResult


class CreateAccountHandlerContract(ABC):
    """Contract for create account command handler"""

    @abstractmethod
    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        """
        Handle the create account command

        Args:
            command: The create account command

        Returns:
            CreateAccountResult with the new account ID

        Raises:
            ValueError if account creation fails
        """
        pass
