from app.context.user_account.application.commands.delete_account_command import (
    DeleteAccountCommand,
)
from app.context.user_account.application.contracts.delete_account_handler_contract import (
    DeleteAccountHandlerContract,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    UserAccountUserID,
)


class DeleteAccountHandler(DeleteAccountHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, command: DeleteAccountCommand) -> bool:
        # Call repository directly - no complex business logic needed
        return await self._repository.delete_account(
            account_id=UserAccountID(command.account_id),
            user_id=UserAccountUserID(command.user_id),
        )
