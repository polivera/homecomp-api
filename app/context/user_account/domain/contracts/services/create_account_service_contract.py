from abc import ABC, abstractmethod

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency


class CreateAccountServiceContract(ABC):
    """Contract for create account service"""

    @abstractmethod
    async def create_account(
        self, user_id: UserID, name: AccountName, currency: Currency, balance: Balance
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
            ValueError if account with same name already exists for user
        """
        pass
