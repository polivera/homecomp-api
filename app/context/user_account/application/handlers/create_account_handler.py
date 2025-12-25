from app.context.user_account.application.commands.create_account_command import CreateAccountCommand
from app.context.user_account.application.contracts.create_account_handler_contract import (
    CreateAccountHandlerContract,
)
from app.context.user_account.application.dto.create_account_result import CreateAccountResult
from app.context.user_account.domain.contracts.services.create_account_service_contract import (
    CreateAccountServiceContract,
)


class CreateAccountHandler(CreateAccountHandlerContract):
    """Handler for create account command"""

    def __init__(self, service: CreateAccountServiceContract):
        self._service = service

    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        """Execute the create account command"""

        account_id = await self._service.create_account(
            user_id=command.user_id,
            name=command.name,
            currency=command.currency,
            balance=command.balance,
        )

        return CreateAccountResult(account_id=account_id)
