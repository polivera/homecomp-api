from app.context.user_account.application.commands.update_account_command import (
    UpdateAccountCommand,
)
from app.context.user_account.application.contracts.update_account_handler_contract import (
    UpdateAccountHandlerContract,
)
from app.context.user_account.application.dto.update_account_result import (
    UpdateAccountResult,
)
from app.context.user_account.domain.contracts.services.update_account_service_contract import (
    UpdateAccountServiceContract,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)


class UpdateAccountHandler(UpdateAccountHandlerContract):
    def __init__(self, service: UpdateAccountServiceContract):
        self._service = service

    async def handle(self, command: UpdateAccountCommand) -> UpdateAccountResult:
        updated = await self._service.update_account(
            account_id=UserAccountID(command.account_id),
            user_id=UserAccountUserID(command.user_id),
            name=AccountName(command.name),
            currency=UserAccountCurrency(command.currency),
            balance=UserAccountBalance.from_float(command.balance),
        )

        return UpdateAccountResult(
            account_id=updated.account_id, message="Account updated successfully"
        )
