from abc import ABC, abstractmethod

from app.context.user_account.application.commands.update_account_command import (
    UpdateAccountCommand,
)
from app.context.user_account.application.dto.update_account_result import (
    UpdateAccountResult,
)


class UpdateAccountHandlerContract(ABC):
    @abstractmethod
    async def handle(self, command: UpdateAccountCommand) -> UpdateAccountResult:
        pass
