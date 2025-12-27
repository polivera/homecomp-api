from app.context.user_account.application.commands import (
    DeleteAccountCommand,
)
from app.context.user_account.application.contracts import (
    DeleteAccountHandlerContract,
)
from app.context.user_account.application.dto import (
    DeleteAccountErrorCode,
    DeleteAccountResult,
)
from app.context.user_account.domain.contracts.infrastructure import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    UserAccountUserID,
)


class DeleteAccountHandler(DeleteAccountHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, command: DeleteAccountCommand) -> DeleteAccountResult:
        """Execute the delete account command"""

        try:
            success = await self._repository.delete_account(
                account_id=UserAccountID(command.account_id),
                user_id=UserAccountUserID(command.user_id),
            )

            if not success:
                return DeleteAccountResult(
                    error_code=DeleteAccountErrorCode.NOT_FOUND,
                    error_message="Account not found",
                )

            return DeleteAccountResult(success=True)
        except Exception:
            return DeleteAccountResult(
                error_code=DeleteAccountErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
