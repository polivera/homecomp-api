from abc import ABC, abstractmethod

from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)


class UpdateAccountServiceContract(ABC):
    @abstractmethod
    async def update_account(
        self,
        account_id: UserAccountID,
        user_id: UserAccountUserID,
        name: AccountName,
        currency: UserAccountCurrency,
        balance: UserAccountBalance,
    ) -> UserAccountDTO:
        pass
