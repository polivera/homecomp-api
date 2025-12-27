from dataclasses import dataclass
from typing import Optional

from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountDeletedAt,
    UserAccountID,
    UserAccountUserID,
)


@dataclass(frozen=True)
class UserAccountDTO:
    """Domain DTO for user account entity"""

    user_id: UserAccountUserID
    name: AccountName
    currency: UserAccountCurrency
    balance: UserAccountBalance
    account_id: Optional[UserAccountID] = None
    deleted_at: Optional[UserAccountDeletedAt] = None
