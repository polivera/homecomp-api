from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.contracts.services.create_account_service_contract import (
    CreateAccountServiceContract,
)
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountUserID,
)
from app.context.user_account.domain.value_objects.account_name import AccountName


class CreateAccountService(CreateAccountServiceContract):
    """Service for creating user accounts"""

    def __init__(self, account_repository: UserAccountRepositoryContract):
        self._account_repository = account_repository

    async def create_account(
        self,
        user_id: UserAccountUserID,
        name: AccountName,
        currency: UserAccountCurrency,
        balance: UserAccountBalance,
    ) -> UserAccountDTO:
        """Create a new user account with validation"""

        # Create new account DTO (without ID, will be assigned by database)
        account_dto = UserAccountDTO(
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )

        # Save and return the new account ID
        return await self._account_repository.save_account(account_dto)
