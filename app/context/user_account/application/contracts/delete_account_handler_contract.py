from abc import ABC, abstractmethod

from app.context.user_account.application.commands import (
    DeleteAccountCommand,
)
from app.context.user_account.application.dto import (
    DeleteAccountResult,
)


class DeleteAccountHandlerContract(ABC):
    @abstractmethod
    async def handle(self, command: DeleteAccountCommand) -> DeleteAccountResult:
        pass
