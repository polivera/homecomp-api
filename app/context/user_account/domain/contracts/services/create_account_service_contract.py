from abc import ABC, abstractmethod

from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountUserID,
)


class CreateAccountServiceContract(ABC):
    """Contract for create account service"""

    @abstractmethod
    async def create_account(
        self,
        user_id: UserAccountUserID,
        name: AccountName,
        currency: UserAccountCurrency,
        balance: UserAccountBalance,
    ) -> UserAccountDTO:
        """
        Create a new user account

        Args:
            user_id: ID of the user who owns the account
            name: Name of the account
            currency: Currency code for the account
            balance: Initial balance

        Returns:
            AccountID of the created account

        Raises:
            UserAccountMapperError if cannot map model to dto
            UserAccountNameAlreadyExistError if account name already exist
        """
        pass
