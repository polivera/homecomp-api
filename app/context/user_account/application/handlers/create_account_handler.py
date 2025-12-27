from app.context.user_account.application.commands import (
    CreateAccountCommand,
)
from app.context.user_account.application.contracts import (
    CreateAccountHandlerContract,
)
from app.context.user_account.application.dto import (
    CreateAccountErrorCode,
    CreateAccountResult,
)
from app.context.user_account.domain.contracts.services import (
    CreateAccountServiceContract,
)
from app.context.user_account.domain.exceptions import (
    UserAccountMapperError,
    UserAccountNameAlreadyExistError,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountUserID,
)


class CreateAccountHandler(CreateAccountHandlerContract):
    """Handler for create account command"""

    def __init__(self, service: CreateAccountServiceContract):
        self._service = service

    async def handle(self, command: CreateAccountCommand) -> CreateAccountResult:
        """Execute the create account command"""

        try:
            account_dto = await self._service.create_account(
                user_id=UserAccountUserID(command.user_id),
                name=AccountName(command.name),
                currency=UserAccountCurrency(command.currency),
                balance=UserAccountBalance.from_float(command.balance),
            )

            if account_dto.account_id is None:
                return CreateAccountResult(
                    error_code=CreateAccountErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating account",
                )

            return CreateAccountResult(
                account_id=account_dto.account_id.value,
                account_name=account_dto.name.value,
                account_balance=float(account_dto.balance.value),
            )
        except UserAccountNameAlreadyExistError:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.NAME_ALREADY_EXISTS,
                error_message="Account name already exist",
            )
        except UserAccountMapperError:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )
        except Exception:
            return CreateAccountResult(
                error_code=CreateAccountErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
