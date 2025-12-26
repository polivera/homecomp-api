from dataclasses import dataclass

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.value_objects.account_id import AccountID


@dataclass(frozen=True)
class FindAccountByIdQuery:
    account_id: AccountID
    user_id: UserID
