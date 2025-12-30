from app.context.user_account.application.commands import (
    UpdateAccountCommand,
)
from app.context.user_account.application.contracts import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.application.dto import (
    UpdateAccountErrorCode,
    UpdateAccountResult,
)
from app.context.user_account.domain.contracts.services import (
    UpdateAccountServiceContract,
)
from app.context.user_account.domain.exceptions import (
    UserAccountMapperError,
    UserAccountNameAlreadyExistError,
    UserAccountNotFoundError,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)
from app.shared.domain.contracts import LoggerContract


class UpdateAccountHandler(UpdateAccountHandlerContract):
    def __init__(self, service: UpdateAccountServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: UpdateAccountCommand) -> UpdateAccountResult:
        """Execute the update account command"""

        try:
            updated = await self._service.update_account(
                account_id=UserAccountID(command.account_id),
                user_id=UserAccountUserID(command.user_id),
                name=AccountName(command.name),
                currency=UserAccountCurrency(command.currency),
                balance=UserAccountBalance.from_float(command.balance),
            )

            if updated.account_id is None:
                self._logger.error(
                    "Account update returned None account_id",
                    account_id=command.account_id,
                    user_id=command.user_id,
                )
                return UpdateAccountResult(
                    error_code=UpdateAccountErrorCode.UNEXPECTED_ERROR,
                    error_message="Error updating account",
                )

            return UpdateAccountResult(
                account_id=updated.account_id.value,
                account_name=updated.name.value,
                account_balance=float(updated.balance.value),
            )
        except UserAccountNotFoundError:
            return UpdateAccountResult(
                error_code=UpdateAccountErrorCode.NOT_FOUND,
                error_message="Account not found",
            )
        except UserAccountNameAlreadyExistError:
            return UpdateAccountResult(
                error_code=UpdateAccountErrorCode.NAME_ALREADY_EXISTS,
                error_message="Account name already exist",
            )
        except UserAccountMapperError:
            return UpdateAccountResult(
                error_code=UpdateAccountErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )
        except Exception as e:
            self._logger.error(
                "Unexpected error during account update",
                account_id=command.account_id,
                user_id=command.user_id,
                error=str(e),
            )
            return UpdateAccountResult(
                error_code=UpdateAccountErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
