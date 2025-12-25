from dataclasses import dataclass

from app.context.user_account.domain.value_objects.account_id import AccountID


@dataclass(frozen=True)
class CreateAccountResult:
    """Result of account creation operation"""

    account_id: AccountID
    message: str = "Account created successfully"
