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


class UpdateAccountHandler(UpdateAccountHandlerContract):
    def __init__(self, service: UpdateAccountServiceContract):
        self._service = service

    async def handle(self, command: UpdateAccountCommand) -> UpdateAccountResult:
        updated = await self._service.update_account(
            account_id=command.account_id,
            user_id=command.user_id,
            name=command.name,
            currency=command.currency,
            balance=command.balance,
        )

        return UpdateAccountResult(
            account_id=updated.account_id, message="Account updated successfully"
        )
