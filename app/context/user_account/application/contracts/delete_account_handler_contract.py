from abc import ABC, abstractmethod

from app.context.user_account.application.commands.delete_account_command import (
    DeleteAccountCommand,
)


class DeleteAccountHandlerContract(ABC):
    @abstractmethod
    async def handle(self, command: DeleteAccountCommand) -> bool:
        pass
