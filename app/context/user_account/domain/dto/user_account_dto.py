from dataclasses import dataclass
from typing import Optional

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency


@dataclass(frozen=True)
class UserAccountDTO:
    """Domain DTO for user account entity"""

    user_id: UserID
    name: AccountName
    currency: Currency
    balance: Balance
    account_id: Optional[AccountID] = None
