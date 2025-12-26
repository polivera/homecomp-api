from abc import ABC, abstractmethod

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency


class UpdateAccountServiceContract(ABC):
    @abstractmethod
    async def update_account(
        self,
        account_id: AccountID,
        user_id: UserID,
        name: AccountName,
        currency: Currency,
        balance: Balance,
    ) -> UserAccountDTO:
        pass
