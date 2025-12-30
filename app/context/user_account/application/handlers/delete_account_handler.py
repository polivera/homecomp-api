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
from app.shared.domain.contracts import LoggerContract


class DeleteAccountHandler(DeleteAccountHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

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
        except Exception as e:
            self._logger.error(
                "Unexpected error during account deletion",
                account_id=command.account_id,
                user_id=command.user_id,
                error=str(e),
            )
            return DeleteAccountResult(
                error_code=DeleteAccountErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
